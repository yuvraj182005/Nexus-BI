"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { MetricCard } from "@/components/common/metric-card";
import { EChart, createAreaChartOption } from "@/components/charts/echart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Activity, Cpu, Database, Server, Zap } from "lucide-react";

export default function RealtimeMonitoringPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Real-Time Telemetry & Monitoring"
        description="Live streaming data pipeline metrics, API latency bounds, memory utilization, and system health."
      />

      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard label="System Status" value="Healthy" change={0} changeType="neutral" icon={Server} delay={0} />
          <MetricCard label="API P99 Latency" value="12ms" change={4.2} changeType="decrease" icon={Zap} delay={0.1} />
          <MetricCard label="Active Streaming Connections" value={1420} change={12.5} changeType="increase" icon={Activity} delay={0.2} />
          <MetricCard label="CPU Utilization" value="24.8%" change={1.2} changeType="decrease" icon={Cpu} delay={0.3} />
        </div>
      </PageSection>

      <PageSection>
        <Card className="glass-panel border-white/[0.08]">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <Activity className="h-4 w-4 text-emerald-400" /> Live Ingestion Telemetry Stream
            </CardTitle>
            <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px] gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" /> Real-time Stream
            </Badge>
          </CardHeader>
          <CardContent>
            <EChart
              option={createAreaChartOption(
                ["12:00", "12:05", "12:10", "12:15", "12:20", "12:25", "12:30"],
                [{ name: "Events/sec", data: [4200, 5800, 6100, 5400, 7200, 6900, 8100], color: "#10b981" }]
              )}
              height={300}
            />
          </CardContent>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
