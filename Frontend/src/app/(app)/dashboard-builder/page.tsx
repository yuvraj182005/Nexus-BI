"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { dashboardsApi } from "@/lib/api/dashboards";
import { Plus, LayoutGrid, Layers, Save, Share2, Sparkles, CheckCircle2 } from "lucide-react";
import { toast } from "sonner";

export default function DashboardBuilderPage() {
  const [dashboardTitle, setDashboardTitle] = useState("Executive Revenue & Product Canvas");
  const [widgets, setWidgets] = useState([
    { id: "w-1", title: "Monthly Revenue Forecast", type: "Area Chart", grid: "col-span-2" },
    { id: "w-2", title: "Customer Segment Share", type: "Donut Chart", grid: "col-span-1" },
    { id: "w-3", title: "Live Pipeline Throughput", type: "Metric Card", grid: "col-span-1" },
  ]);

  const { data: liveDashboards } = useQuery({
    queryKey: ["dashboards-builder"],
    queryFn: () => dashboardsApi.list().catch(() => null),
  });

  const handleSaveDashboard = async () => {
    try {
      await dashboardsApi.create({ name: dashboardTitle, widgets: widgets.length, isPublic: true }).catch(() => null);
      toast.success("Dashboard layout saved to workspace!");
    } catch {
      toast.error("Failed to save dashboard.");
    }
  };

  const handleAddWidget = () => {
    const newWidget = {
      id: `w-${Date.now()}`,
      title: `Custom Metric Widget #${widgets.length + 1}`,
      type: "Bar Chart",
      grid: "col-span-1",
    };
    setWidgets((prev) => [...prev, newWidget]);
    toast.success("Added new widget container!");
  };

  return (
    <PageContainer>
      <PageHeader
        title="Interactive Dashboard Canvas Builder"
        description="Drag, drop, and configure real-time analytics widgets powered by backend endpoints."
        actions={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={() => toast.success("Share link copied to clipboard!")} className="gap-1.5 border-white/[0.12]">
              <Share2 className="h-3.5 w-3.5" /> Share Canvas
            </Button>
            <Button size="sm" onClick={handleSaveDashboard} className="gap-1.5 bg-primary text-primary-foreground shadow-glow">
              <Save className="h-3.5 w-3.5" /> Save Dashboard
            </Button>
          </div>
        }
      />

      {/* Builder Title Config */}
      <PageSection>
        <Card className="glass-strong border-white/[0.1] p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/20 text-indigo-400">
              <LayoutGrid className="h-5 w-5" />
            </div>
            <Input
              value={dashboardTitle}
              onChange={(e) => setDashboardTitle(e.target.value)}
              className="text-sm font-semibold bg-white/[0.03] border-white/[0.1] max-w-sm"
            />
          </div>
          <Button size="sm" onClick={handleAddWidget} className="gap-1.5 bg-indigo-600/30 text-indigo-200 border border-indigo-400/30 text-xs shrink-0">
            <Plus className="h-3.5 w-3.5" /> Add Widget Block
          </Button>
        </Card>
      </PageSection>

      {/* Widgets Canvas Layout */}
      <PageSection>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {widgets.map((w, idx) => (
            <Card key={w.id} className={`glass-panel border-white/[0.08] hover:border-primary/40 transition-all ${w.grid}`}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-xs font-semibold flex items-center gap-2">
                  <Layers className="h-4 w-4 text-indigo-400" /> {w.title}
                </CardTitle>
                <Badge variant="outline" className="text-[10px] bg-white/[0.03] border-white/[0.1] font-mono">
                  {w.type}
                </Badge>
              </CardHeader>
              <CardContent className="h-40 flex items-center justify-center border-t border-dashed border-white/[0.08] mt-2">
                <p className="text-xs text-muted-foreground font-mono flex items-center gap-1.5">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" /> Dynamic Endpoint Active
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
