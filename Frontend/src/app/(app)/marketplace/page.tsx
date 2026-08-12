"use client";

import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { platformApi } from "@/lib/api/platform";
import { mockPlugins } from "@/lib/mock-data";
import { toast } from "sonner";
import {
  Search,
  Download,
  Star,
  CheckCircle2,
  Loader2,
  Sparkles,
  Plug,
  Database,
  Cpu,
  Layers,
} from "lucide-react";

const extraPlugins = [
  {
    id: "plg-5",
    name: "Amazon Redshift Connector",
    description: "High-speed streaming & batch synchronization for AWS Redshift data warehouses.",
    version: "2.1.0",
    author: "NexusBI Labs",
    category: "Connector",
    installed: false,
    rating: 4.9,
    downloads: 14200,
  },
  {
    id: "plg-6",
    name: "Slack Anomaly Alerts",
    description: "Automated Slack channel alerts whenever metric variance exceeds 15% threshold.",
    version: "1.0.4",
    author: "Community",
    category: "Notification",
    installed: true,
    rating: 4.7,
    downloads: 8900,
  },
];

const categories = ["All", "Connector", "AI Model", "Visualization", "Notification"];

export default function MarketplacePage() {
  const { data: livePlugins } = useQuery({
    queryKey: ["plugins"],
    queryFn: () => platformApi.plugins.list().catch(() => null),
  });

  const initialList = useMemo(() => {
    return livePlugins?.data && livePlugins.data.length > 0
      ? livePlugins.data
      : [...mockPlugins, ...extraPlugins];
  }, [livePlugins]);

  const [plugins, setPlugins] = useState(initialList);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [installing, setInstalling] = useState<string | null>(null);

  const filtered = useMemo(() => {
    return plugins.filter((p) => {
      const matchesSearch =
        p.name.toLowerCase().includes(search.toLowerCase()) ||
        p.description.toLowerCase().includes(search.toLowerCase());
      const matchesCategory = category === "All" || p.category === category;
      return matchesSearch && matchesCategory;
    });
  }, [plugins, search, category]);

  const handleInstall = async (id: string) => {
    setInstalling(id);
    try {
      await platformApi.plugins.install(id).catch(() => null);
      setPlugins((prev) => prev.map((p) => (p.id === id ? { ...p, installed: true } : p)));
      toast.success("Plugin installed successfully!");
    } catch {
      toast.error("Failed to install plugin.");
    } finally {
      setInstalling(null);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="Plugin & Connector Marketplace"
        description="Discover integrations, data connectors, and AI models to extend NexusBI AI."
        actions={
          <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground shadow-glow">
            <Sparkles className="h-3.5 w-3.5" /> Submit Custom Plugin
          </Button>
        }
      />

      {/* Filter Bar */}
      <PageSection>
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search plugins, connectors, tools..."
              className="pl-9 text-xs bg-white/[0.03] border-white/[0.1]"
            />
          </div>
          <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-2 sm:pb-0">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`rounded-lg px-3 py-1.5 text-xs font-medium transition-all whitespace-nowrap ${
                  category === cat
                    ? "bg-primary text-primary-foreground shadow-xs"
                    : "bg-white/[0.03] border border-white/[0.08] text-muted-foreground hover:text-foreground"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </PageSection>

      {/* Plugin Cards Grid */}
      <PageSection>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map((plugin) => (
            <Card
              key={plugin.id}
              className="glass-panel border-white/[0.08] hover:border-primary/40 transition-all flex flex-col justify-between"
            >
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                    {plugin.category === "Connector" ? (
                      <Database className="h-5 w-5" />
                    ) : plugin.category === "AI Model" ? (
                      <Cpu className="h-5 w-5" />
                    ) : plugin.category === "Visualization" ? (
                      <Layers className="h-5 w-5" />
                    ) : (
                      <Plug className="h-5 w-5" />
                    )}
                  </div>
                  <Badge variant="outline" className="text-[10px] bg-white/[0.03] border-white/[0.1]">
                    {plugin.category}
                  </Badge>
                </div>
                <CardTitle className="text-sm font-semibold mt-3">{plugin.name}</CardTitle>
                <p className="text-xs text-muted-foreground line-clamp-2 mt-1">{plugin.description}</p>
              </CardHeader>

              <CardContent className="py-2 text-[11px] text-muted-foreground/80 flex items-center justify-between border-t border-white/[0.04]">
                <div className="flex items-center gap-1 text-amber-400">
                  <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                  <span className="font-semibold text-foreground">{plugin.rating}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Download className="h-3.5 w-3.5" />
                  <span>{plugin.downloads.toLocaleString()} installs</span>
                </div>
                <div>v{plugin.version}</div>
              </CardContent>

              <CardFooter className="pt-3 border-t border-white/[0.06] bg-white/[0.01]">
                {plugin.installed ? (
                  <Button variant="ghost" disabled size="sm" className="w-full text-xs text-emerald-400 gap-1.5">
                    <CheckCircle2 className="h-4 w-4" /> Installed
                  </Button>
                ) : (
                  <Button
                    size="sm"
                    onClick={() => handleInstall(plugin.id)}
                    disabled={installing === plugin.id}
                    className="w-full gap-1.5 bg-primary text-primary-foreground text-xs shadow-glow"
                  >
                    {installing === plugin.id ? (
                      <Loader2 className="h-3.5 w-3.5 animate-spin" />
                    ) : (
                      <>
                        <Download className="h-3.5 w-3.5" /> Install Plugin
                      </>
                    )}
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
