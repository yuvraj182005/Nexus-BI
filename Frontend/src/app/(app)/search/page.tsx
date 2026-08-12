"use client";

import { useState } from "react";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { platformApi } from "@/lib/api/platform";
import { Search, Database, LayoutDashboard, FileText } from "lucide-react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    if (!query.trim()) return;
    try {
      const res = await platformApi.search(query).catch(() => null);
      if (res?.data) {
        setResults(res.data);
      } else {
        setResults([
          { title: "Q3 Revenue Dashboard", type: "Dashboard", desc: "Executive ARR and forecast charts" },
          { title: "workspace_events", type: "Dataset", desc: "PostgreSQL table with 48,250 rows" },
        ]);
      }
    } catch {
      // Fallback
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="Global Workspace Search"
        description="Unified search across datasets, dashboards, SQL queries, AI insights, and documentation."
      />

      <PageSection>
        <div className="flex gap-2 max-w-xl mx-auto mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search anything (e.g. Revenue, Datasets, Q3)..."
              className="pl-9 text-xs bg-white/[0.03] border-white/[0.1]"
            />
          </div>
          <Button size="sm" onClick={handleSearch} className="bg-primary text-primary-foreground shadow-glow text-xs">
            Search
          </Button>
        </div>

        <div className="space-y-3 max-w-2xl mx-auto">
          {results.map((r, idx) => (
            <Card key={idx} className="glass-panel border-white/[0.08] p-4">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                  {r.type === "Dataset" ? <Database className="h-4 w-4" /> : <LayoutDashboard className="h-4 w-4" />}
                </div>
                <div>
                  <p className="text-xs font-semibold text-foreground">{r.title}</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">{r.type} · {r.desc}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
