"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { MetricCard } from "@/components/common/metric-card";
import { ActivityFeed } from "@/components/common/activity-feed";
import { EChart, createAreaChartOption, createPieChartOption } from "@/components/charts/echart";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { platformApi } from "@/lib/api/platform";
import { dashboardsApi } from "@/lib/api/dashboards";
import { mockMetrics, mockActivities, chartData, mockDashboards } from "@/lib/mock-data";
import {
  DollarSign,
  Users,
  Database,
  Bot,
  Plus,
  ArrowUpRight,
  Sparkles,
  Clock,
  Layers,
} from "lucide-react";
import Link from "next/link";
import { ROUTES } from "@/lib/constants";
import { useUIStore } from "@/stores/ui-store";

const metricIcons = [DollarSign, Users, Database, Bot];

export default function DashboardPage() {
  const [timeframe, setTimeframe] = useState<"7D" | "30D" | "90D" | "YTD">("30D");
  const { toggleCopilot } = useUIStore();

  // Consume live metrics API from FastAPI
  const { data: liveMetrics } = useQuery({
    queryKey: ["metrics"],
    queryFn: () => platformApi.metrics().catch(() => null),
  });

  // Consume dashboards list API from FastAPI
  const { data: liveDashboards } = useQuery({
    queryKey: ["dashboards"],
    queryFn: () => dashboardsApi.list().catch(() => null),
  });

  // Consume audit logs API from FastAPI
  const { data: liveAudit } = useQuery({
    queryKey: ["audit-logs"],
    queryFn: () => platformApi.audit.list().catch(() => null),
  });

  const dashboards = liveDashboards?.data || mockDashboards;
  const activities = liveAudit?.data?.map((a) => ({
    id: a.id,
    type: a.action,
    title: a.action,
    description: a.details || `${a.user} performed ${a.action} on ${a.resource}`,
    user: a.user,
    timestamp: a.timestamp,
  })) || mockActivities;

  return (
    <PageContainer>
      <PageHeader
        title="Executive BI Dashboard"
        description="Real-time analytics, revenue forecasting, data volume, and AI decision intelligence."
        actions={
          <div className="flex items-center gap-2">
            <div className="hidden sm:flex items-center rounded-lg border border-white/[0.08] bg-white/[0.03] p-1">
              {(["7D", "30D", "90D", "YTD"] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setTimeframe(t)}
                  className={`rounded-md px-2.5 py-1 text-xs font-medium transition-all ${
                    timeframe === t
                      ? "bg-primary text-primary-foreground shadow-xs"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
            <Link href={ROUTES.datasetUpload}>
              <Button variant="outline" size="sm" className="gap-1.5 border-white/[0.12] bg-white/[0.03] hover:bg-white/[0.08]">
                <Plus className="h-3.5 w-3.5" /> Upload Data
              </Button>
            </Link>
            <Link href={ROUTES.dashboardBuilder}>
              <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground shadow-glow">
                <Plus className="h-3.5 w-3.5" /> New Dashboard
              </Button>
            </Link>
          </div>
        }
      />

      {/* AI Copilot Callout Banner */}
      <div className="relative overflow-hidden rounded-2xl glass-strong border border-indigo-500/20 p-4 md:p-5 shadow-glow mb-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative z-10">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/30 to-purple-500/30 border border-indigo-400/30">
              <Sparkles className="h-5 w-5 text-indigo-400 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-semibold text-foreground">AI Insight Detected</h3>
                <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                  98.4% Confidence
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5">
                Q3 enterprise expansion projected to boost ARR by <span className="text-emerald-400 font-semibold">+18.2%</span>. Request AI analysis for details.
              </p>
            </div>
          </div>
          <Button
            size="sm"
            onClick={toggleCopilot}
            className="gap-2 bg-indigo-600/30 hover:bg-indigo-600/50 text-indigo-200 border border-indigo-400/30 text-xs shrink-0"
          >
            Ask AI Copilot <ArrowUpRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>

      {/* KPI Metric Cards */}
      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {mockMetrics.slice(0, 4).map((metric, i) => {
            const apiVal = liveMetrics?.data ? Object.values(liveMetrics.data)[i] : undefined;
            const val = apiVal !== undefined ? apiVal : metric.value;
            return (
              <MetricCard key={metric.label} {...metric} value={val} icon={metricIcons[i]} delay={i * 0.1} />
            );
          })}
        </div>
      </PageSection>

      {/* Interactive Charts Section */}
      <div className="grid lg:grid-cols-3 gap-6">
        <PageSection className="lg:col-span-2">
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div>
                <CardTitle className="text-base font-semibold">Revenue Trend & AI Forecast</CardTitle>
                <p className="text-xs text-muted-foreground mt-0.5">Monthly revenue vs forecasted growth model</p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/30 text-[10px] gap-1">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" /> Live Pipeline
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <EChart
                option={createAreaChartOption(
                  chartData.revenue.map((d) => d.month),
                  [
                    { name: "Actual ARR", data: chartData.revenue.map((d) => d.value), color: "#6366f1" },
                    { name: "AI Projected", data: chartData.revenue.map((d) => d.forecast), color: "#10b981" },
                  ]
                )}
                height={320}
              />
            </CardContent>
          </Card>
        </PageSection>

        <PageSection>
          <Card className="glass-panel border-white/[0.08] h-full flex flex-col justify-between">
            <CardHeader className="pb-2">
              <CardTitle className="text-base font-semibold">Customer Segment Share</CardTitle>
              <p className="text-xs text-muted-foreground">ARR distribution by client tier</p>
            </CardHeader>
            <CardContent className="flex-1 flex items-center justify-center">
              <EChart
                option={createPieChartOption(chartData.categories, { donut: true })}
                height={280}
              />
            </CardContent>
          </Card>
        </PageSection>
      </div>

      {/* Dashboards Grid & Activity Feed */}
      <div className="grid lg:grid-cols-2 gap-6 mt-2">
        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-base font-semibold font-sans">Recent Dashboards</CardTitle>
                <p className="text-xs text-muted-foreground">Active workspace visualizations</p>
              </div>
              <Link href={ROUTES.dashboardBuilder}>
                <Button variant="ghost" size="sm" className="gap-1 text-xs text-indigo-400 hover:text-indigo-300">
                  View all <ArrowUpRight className="h-3 w-3" />
                </Button>
              </Link>
            </CardHeader>
            <CardContent className="space-y-3">
              {dashboards.slice(0, 4).map((dash) => (
                <div
                  key={dash.id}
                  className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5 hover:border-primary/30 hover:bg-white/[0.04] transition-all duration-200"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                      <Layers className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-foreground">{dash.name}</p>
                      <p className="text-[10px] text-muted-foreground mt-0.5">
                        {dash.widgets} widgets · {dash.views?.toLocaleString() || 0} views
                      </p>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-[10px] bg-white/[0.03] border-white/[0.1]">
                    {dash.tags?.[0] || "Analytics"}
                  </Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </PageSection>

        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle className="text-base font-semibold">Live Audit & Activity</CardTitle>
                <p className="text-xs text-muted-foreground">Real-time user & automated system actions</p>
              </div>
              <Badge variant="outline" className="text-[10px] text-muted-foreground gap-1">
                <Clock className="h-3 w-3" /> Real-time
              </Badge>
            </CardHeader>
            <CardContent>
              <ActivityFeed items={activities} />
            </CardContent>
          </Card>
        </PageSection>
      </div>
    </PageContainer>
  );
}
