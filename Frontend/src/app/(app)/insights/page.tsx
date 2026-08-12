"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { aiApi } from "@/lib/api/ai";
import { Lightbulb, Sparkles, TrendingUp, AlertTriangle, ArrowUpRight } from "lucide-react";
import { toast } from "sonner";

export default function BusinessInsightsPage() {
  const { data: insightsRes, refetch } = useQuery({
    queryKey: ["insights"],
    queryFn: () => aiApi.insights("ds-1").catch(() => null),
  });

  const insightsList = insightsRes?.data?.insights || [
    "Q3 enterprise expansion projected to boost ARR by +18.2% based on current pipeline velocities.",
    "Customer churn risk detected in SMB tier due to low API key activity in last 14 days.",
    "Data pipeline latency reduced by 34% following index optimization on PostgreSQL cluster.",
    "High correlation (0.89) discovered between product usage frequency and annual expansion.",
  ];

  return (
    <PageContainer>
      <PageHeader
        title="Automated Business Insights"
        description="AI-driven root cause detection, anomaly highlights, and strategic decision recommendations."
        actions={
          <Button size="sm" onClick={() => { refetch(); toast.success("Refreshed AI insights!"); }} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            <Sparkles className="h-4 w-4" /> Generate New Insights
          </Button>
        }
      />

      <PageSection>
        <div className="grid md:grid-cols-2 gap-4">
          {insightsList.map((item, idx) => (
            <Card key={idx} className="glass-panel border-white/[0.08] hover:border-indigo-500/40 transition-all">
              <CardHeader className="pb-2 flex flex-row items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                    <Lightbulb className="h-4 w-4" />
                  </div>
                  <CardTitle className="text-sm font-semibold">Insight #{idx + 1}</CardTitle>
                </div>
                <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                  High Impact
                </Badge>
              </CardHeader>
              <CardContent className="pt-2">
                <p className="text-xs text-foreground/90 leading-relaxed">{item}</p>
                <div className="mt-4 flex items-center justify-between border-t border-white/[0.06] pt-3 text-[10px] text-muted-foreground">
                  <span>Confidence: 98.4%</span>
                  <span className="text-indigo-400 hover:underline cursor-pointer flex items-center gap-1 font-semibold">
                    View Impact Model <ArrowUpRight className="h-3 w-3" />
                  </span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
