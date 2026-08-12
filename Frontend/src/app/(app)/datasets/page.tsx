"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { DatasetCard } from "@/components/common/dataset-card";
import { MetricCard } from "@/components/common/metric-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { mockDatasets } from "@/lib/mock-data";
import { ROUTES } from "@/lib/constants";
import { formatBytes } from "@/lib/utils";
import {
  Plus,
  Search,
  Filter,
  Database,
  HardDrive,
  CheckCircle2,
  Loader2,
  LayoutGrid,
  List,
  Sparkles,
  Server,
  Cloud,
} from "lucide-react";

type StatusFilter = "all" | "active" | "processing" | "error";
type TypeFilter = "all" | "csv" | "json" | "parquet" | "sql";

export default function DatasetsPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [typeFilter, setTypeFilter] = useState<TypeFilter>("all");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");

  const filtered = useMemo(() => {
    return mockDatasets.filter((ds) => {
      const matchesSearch =
        ds.name.toLowerCase().includes(search.toLowerCase()) ||
        ds.tags.some((t) => t.toLowerCase().includes(search.toLowerCase())) ||
        ds.createdBy.toLowerCase().includes(search.toLowerCase());
      const matchesStatus = statusFilter === "all" || ds.status === statusFilter;
      const matchesType = typeFilter === "all" || ds.type === typeFilter;
      return matchesSearch && matchesStatus && matchesType;
    });
  }, [search, statusFilter, typeFilter]);

  const totalSize = mockDatasets.reduce((acc, ds) => acc + ds.size, 0);
  const avgQuality = Math.round(mockDatasets.reduce((acc, ds) => acc + ds.quality, 0) / mockDatasets.length);
  const activeCount = mockDatasets.filter((ds) => ds.status === "active").length;
  const processingCount = mockDatasets.filter((ds) => ds.status === "processing").length;

  return (
    <PageContainer>
      <PageHeader
        title="Datasets & Semantic Layer"
        description="Manage, explore, profile, and govern your organization's enterprise data assets."
        actions={
          <div className="flex items-center gap-2">
            <Link href={ROUTES.datasetUpload}>
              <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground shadow-glow">
                <Plus className="h-3.5 w-3.5" /> Upload Dataset
              </Button>
            </Link>
          </div>
        }
      />

      {/* Connection Connectors Summary Banner */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {[
          { name: "PostgreSQL Production", type: "RDBMS", status: "Connected", icon: Server },
          { name: "Snowflake Warehouse", type: "Cloud DW", status: "Connected", icon: Cloud },
          { name: "Google BigQuery", type: "Analytics Engine", status: "Connected", icon: Database },
          { name: "Apache Kafka Stream", type: "Real-time Event", status: "Streaming", icon: Sparkles },
        ].map((c) => (
          <div key={c.name} className="glass-panel border-white/[0.08] p-3 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 shrink-0">
                <c.icon className="h-4 w-4" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold text-foreground truncate">{c.name}</p>
                <p className="text-[10px] text-muted-foreground">{c.type}</p>
              </div>
            </div>
            <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-glow-emerald shrink-0" />
          </div>
        ))}
      </div>

      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard label="Total Data Assets" value={mockDatasets.length} change={20} changeType="increase" icon={Database} />
          <MetricCard label="Total Storage Volume" value={formatBytes(totalSize)} change={15.4} changeType="increase" icon={HardDrive} />
          <MetricCard label="Avg Quality Score" value={`${avgQuality}%`} change={2.3} changeType="increase" icon={CheckCircle2} />
          <MetricCard label="Active Ingestions" value={processingCount} change={0} changeType="neutral" icon={Loader2} />
        </div>
      </PageSection>

      <PageSection>
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search datasets, tags, or owners..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 bg-white/[0.03] border-white/[0.1] text-xs"
            />
          </div>
          <div className="flex items-center gap-2">
            <div className="flex rounded-lg border border-white/[0.1] bg-white/[0.03] p-1">
              {(["all", "active", "processing"] as const).map((st) => (
                <button
                  key={st}
                  onClick={() => setStatusFilter(st)}
                  className={`px-3 py-1 text-xs rounded-md capitalize font-medium transition-all ${
                    statusFilter === st ? "bg-primary text-primary-foreground shadow-xs" : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {st}
                </button>
              ))}
            </div>
            <div className="flex rounded-lg border border-white/[0.1] bg-white/[0.03] p-1">
              <button
                onClick={() => setViewMode("grid")}
                className={`p-1.5 rounded ${viewMode === "grid" ? "bg-primary text-primary-foreground" : "text-muted-foreground"}`}
              >
                <LayoutGrid className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`p-1.5 rounded ${viewMode === "list" ? "bg-primary text-primary-foreground" : "text-muted-foreground"}`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mt-3 items-center">
          <Filter className="h-3.5 w-3.5 text-muted-foreground" />
          {(["all", "csv", "json", "parquet", "sql"] as TypeFilter[]).map((type) => (
            <Badge
              key={type}
              variant={typeFilter === type ? "default" : "outline"}
              className={`cursor-pointer capitalize text-[10px] ${
                typeFilter === type ? "bg-primary text-primary-foreground" : "border-white/[0.1] bg-white/[0.02]"
              }`}
              onClick={() => setTypeFilter(type)}
            >
              {type}
            </Badge>
          ))}
        </div>
      </PageSection>

      <PageSection>
        {filtered.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-white/[0.1] bg-white/[0.01] p-12 text-center">
            <Database className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
            <p className="font-medium text-foreground text-sm">No datasets found</p>
            <p className="text-xs text-muted-foreground mt-1">Try adjusting your search query or clear active filters</p>
          </div>
        ) : viewMode === "grid" ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {filtered.map((dataset, i) => (
              <DatasetCard key={dataset.id} dataset={dataset} delay={i * 0.05} />
            ))}
          </div>
        ) : (
          <div className="space-y-2">
            {filtered.map((dataset, i) => (
              <div
                key={dataset.id}
                className="flex items-center justify-between rounded-xl border border-white/[0.08] bg-white/[0.02] p-4 hover:border-primary/30 transition-all"
              >
                <div className="flex items-center gap-4">
                  <span className="text-xs text-muted-foreground w-6 font-mono">{i + 1}</span>
                  <div>
                    <p className="font-semibold text-xs text-foreground">{dataset.name}</p>
                    <p className="text-[10px] text-muted-foreground">{dataset.createdBy} · {dataset.type.toUpperCase()}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs">
                  <span className="text-muted-foreground hidden sm:inline">{dataset.rows.toLocaleString()} rows</span>
                  <Badge className={dataset.status === "active" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]" : "bg-amber-500/10 text-amber-400 border-amber-500/20 text-[10px]"}>
                    {dataset.status}
                  </Badge>
                  <span className="font-semibold text-indigo-400">{dataset.quality}%</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </PageSection>
    </PageContainer>
  );
}
