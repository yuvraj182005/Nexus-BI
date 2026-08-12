"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { MetricCard } from "@/components/common/metric-card";
import { EChart, createAreaChartOption, createBarChartOption } from "@/components/charts/echart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { platformApi } from "@/lib/api/platform";
import { mockMetrics, chartData } from "@/lib/mock-data";
import { BarChart3, TrendingUp, DollarSign, Users, Database, Sparkles } from "lucide-react";

export default function AnalyticsStudioPage() {
  const { data: liveMetrics } = useQuery({
    queryKey: ["analytics-metrics"],
    queryFn: () => platformApi.metrics().catch(() => null),
  });

  return (
    <PageContainer>
      <PageHeader
        title="Analytics Studio & Intelligence"
        description="Deep data aggregation, multi-dimensional metrics breakdown, and variance analysis."
      />

      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard label="Total Annual Revenue" value="$4,820,500" change={14.2} changeType="increase" icon={DollarSign} delay={0} />
          <MetricCard label="Active Enterprise Seats" value={14280} change={8.4} changeType="increase" icon={Users} delay={0.1} />
          <MetricCard label="Data Pipeline Throughput" value="1.2 TB/s" change={18.0} changeType="increase" icon={Database} delay={0.2} />
          <MetricCard label="Model Confidence" value="99.4%" change={0.5} changeType="increase" icon={Sparkles} delay={0.3} />
        </div>
      </PageSection>

      <div className="grid lg:grid-cols-2 gap-6">
        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-base font-semibold flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-indigo-400" /> Revenue Growth Variance
              </CardTitle>
              <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">Live Data</Badge>
            </CardHeader>
            <CardContent>
              <EChart
                option={createAreaChartOption(
                  chartData.revenue.map((d) => d.month),
                  [
                    { name: "ARR", data: chartData.revenue.map((d) => d.value), color: "#6366f1" },
                    { name: "Forecast", data: chartData.revenue.map((d) => d.forecast), color: "#10b981" },
                  ]
                )}
                height={300}
              />
            </CardContent>
          </Card>
        </PageSection>

        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-base font-semibold flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-cyan-400" /> Segment Performance
              </CardTitle>
            </CardHeader>
            <CardContent>
              <EChart
                option={createBarChartOption(
                  [
                    { name: "Enterprise", value: 2450000 },
                    { name: "Mid-Market", value: 1420000 },
                    { name: "SMB", value: 680000 },
                    { name: "Self-Serve", value: 270000 },
                  ]
                )}
                height={300}
              />
            </CardContent>
          </Card>
        </PageSection>
      </div>
    </PageContainer>
  );
}
