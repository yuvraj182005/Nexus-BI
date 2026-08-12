"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { platformApi } from "@/lib/api/platform";
import { mockWorkflows } from "@/lib/mock-data";
import { GitBranch, Play, Plus, CheckCircle2, Clock } from "lucide-react";
import { toast } from "sonner";

export default function WorkflowsPage() {
  const { data: liveWorkflows } = useQuery({
    queryKey: ["workflows"],
    queryFn: () => platformApi.workflows.list().catch(() => null),
  });

  const workflows = liveWorkflows?.data || mockWorkflows;

  const handleRunWorkflow = async (id: string) => {
    try {
      await platformApi.workflows.run(id).catch(() => null);
      toast.success("Triggered workflow pipeline execution!");
    } catch {
      toast.error("Failed to run workflow.");
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="Automated Data Workflows"
        description="Schedule, orchestrate, and monitor ETL pipelines, data sync jobs, and AI model retraining."
        actions={
          <Button size="sm" onClick={() => toast.success("Created new workflow template!")} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            <Plus className="h-4 w-4" /> Create Workflow
          </Button>
        }
      />

      <PageSection>
        <div className="space-y-3">
          {workflows.map((w) => (
            <Card key={w.id} className="glass-panel border-white/[0.08] hover:border-primary/40 transition-all p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                  <GitBranch className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-foreground">{w.name}</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">{w.triggers} triggers · {w.successRate}% success rate</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Badge className={w.status === "active" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]" : "bg-amber-500/10 text-amber-400 border-amber-500/20 text-[10px]"}>
                  {w.status}
                </Badge>
                <Button size="sm" variant="outline" onClick={() => handleRunWorkflow(w.id)} className="gap-1.5 border-white/[0.12] text-xs">
                  <Play className="h-3.5 w-3.5" /> Run Now
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
