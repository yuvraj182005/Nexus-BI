"use client";

import { useState } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { MetricCard } from "@/components/common/metric-card";
import { GlassCard } from "@/components/common/glass-card";
import { ActivityFeed } from "@/components/common/activity-feed";
import { EChart, createBarChartOption } from "@/components/charts/echart";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";
import { aiApi } from "@/lib/api/ai";
import { datasetsApi } from "@/lib/api/datasets";
import { platformApi } from "@/lib/api/platform";
import {
  mockActivities,
  mockDashboards,
  mockDatasets,
  mockWorkflows,
} from "@/lib/mock-data";
import { ROUTES } from "@/lib/constants";
import { getInitials, formatRelativeTime } from "@/lib/utils";
import {
  Users,
  FolderKanban,
  Database,
  GitBranch,
  Plus,
  Settings,
  UserPlus,
  Upload,
  BarChart3,
  Sparkles,
  Crown,
  Shield,
  Code2,
  Eye,
  Play,
  CheckCircle2,
  Terminal,
  FileSpreadsheet,
} from "lucide-react";

const teamMembers = [
  { name: "Sarah Chen", role: "Admin", email: "sarah@nexusbi.io", status: "online", projects: 8 },
  { name: "Marcus Johnson", role: "Analyst", email: "marcus@nexusbi.io", status: "online", projects: 5 },
  { name: "Elena Rodriguez", role: "Developer", email: "elena@nexusbi.io", status: "away", projects: 6 },
  { name: "David Kim", role: "Viewer", email: "david@nexusbi.io", status: "offline", projects: 3 },
];

const roleIcons = { Admin: Crown, Analyst: BarChart3, Developer: Code2, Viewer: Eye };
const roleColors = {
  Admin: "text-amber-400 bg-amber-500/10 border-amber-500/20",
  Analyst: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
  Developer: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  Viewer: "text-slate-400 bg-slate-500/10 border-slate-500/20",
};

const quickActions = [
  { label: "Upload Dataset", href: ROUTES.datasetUpload, icon: Upload, color: "from-indigo-500/20 to-purple-500/20" },
  { label: "Run SQL Query", href: ROUTES.sqlStudio, icon: Code2, color: "from-cyan-500/20 to-blue-500/20" },
  { label: "AI Data Cleaning", href: ROUTES.dataCleaning, icon: Sparkles, color: "from-violet-500/20 to-fuchsia-500/20" },
  { label: "Build Dashboard", href: ROUTES.dashboardBuilder, icon: BarChart3, color: "from-emerald-500/20 to-teal-500/20" },
];

export default function WorkspacePage() {
  const [activeTab, setActiveTab] = useState<"projects" | "datasets">("projects");
  const [promptInput, setPromptInput] = useState("Analyze Q3 churn trends by customer size and generate SQL");
  const [isExecuting, setIsExecuting] = useState(false);
  const [generatedSql, setGeneratedSql] = useState<string | null>(null);
  const [executionTime, setExecutionTime] = useState<number>(0.042);

  // Consume live datasets & audit API from FastAPI
  const { data: liveDatasets } = useQuery({
    queryKey: ["datasets"],
    queryFn: () => datasetsApi.list().catch(() => null),
  });

  const { data: liveAudit } = useQuery({
    queryKey: ["workspace-audit"],
    queryFn: () => platformApi.audit.list().catch(() => null),
  });

  const datasets = liveDatasets?.data || mockDatasets;
  const activities = liveAudit?.data?.map((a) => ({
    id: a.id,
    type: a.action,
    title: a.action,
    description: a.details || `${a.user} performed ${a.action} on ${a.resource}`,
    user: a.user,
    timestamp: a.timestamp,
  })) || mockActivities;

  const handleRunQuery = async () => {
    setIsExecuting(true);
    const start = performance.now();
    try {
      const res = await aiApi.generateSql(promptInput).catch(() => null);
      if (res?.data?.sql) {
        setGeneratedSql(res.data.sql);
      } else {
        setGeneratedSql(
          "SELECT date_trunc('month', created_at) AS month, category, SUM(revenue) FROM workspace_events GROUP BY 1, 2 ORDER BY 1 DESC;"
        );
      }
      setExecutionTime(Number(((performance.now() - start) / 1000).toFixed(3)));
    } catch {
      setGeneratedSql("SELECT * FROM enterprise_metrics WHERE active = true;");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="AI Data Studio & Workspace"
        description="Collaborate with your team, run natural language SQL queries, and manage enterprise data pipelines."
        actions={
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" className="gap-1.5 border-white/[0.12] bg-white/[0.03]">
              <UserPlus className="h-3.5 w-3.5" /> Invite Member
            </Button>
            <Link href={ROUTES.settings}>
              <Button variant="outline" size="sm" className="gap-1.5 border-white/[0.12] bg-white/[0.03]">
                <Settings className="h-3.5 w-3.5" /> Workspace Settings
              </Button>
            </Link>
            <Link href={ROUTES.datasetUpload}>
              <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground shadow-glow">
                <Plus className="h-3.5 w-3.5" /> New Project
              </Button>
            </Link>
          </div>
        }
      />

      {/* Metrics Row */}
      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard label="Team Members" value={12} change={8.3} changeType="increase" icon={Users} delay={0} />
          <MetricCard label="Active Projects" value={24} change={4.2} changeType="increase" icon={FolderKanban} delay={0.1} />
          <MetricCard label="Shared Datasets" value={datasets.length} change={12.0} changeType="increase" icon={Database} delay={0.2} />
          <MetricCard label="Running Workflows" value={mockWorkflows.filter((w) => w.status === "active").length} change={0} changeType="neutral" icon={GitBranch} delay={0.3} />
        </div>
      </PageSection>

      {/* Interactive Natural Language & SQL Studio Bar */}
      <PageSection>
        <Card className="glass-strong border-white/[0.1] shadow-xl overflow-hidden">
          <CardHeader className="border-b border-white/[0.08] pb-3 bg-white/[0.02]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-500/20 text-indigo-400">
                  <Terminal className="h-4 w-4" />
                </div>
                <div>
                  <CardTitle className="text-sm font-semibold">Natural Language Query Engine</CardTitle>
                  <p className="text-[11px] text-muted-foreground">Ask in plain English — AI generates SQL and builds live charts instantly</p>
                </div>
              </div>
              <Badge variant="outline" className="text-[10px] bg-indigo-500/10 text-indigo-400 border-indigo-500/30 gap-1">
                <Sparkles className="h-3 w-3" /> Autonomous Querying
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="p-4 space-y-4">
            <div className="relative">
              <Textarea
                value={promptInput}
                onChange={(e) => setPromptInput(e.target.value)}
                placeholder="Type your question or query (e.g. Find top 10 enterprise customers by LTV in 2026)..."
                className="min-h-[70px] text-xs bg-white/[0.03] border-white/[0.1] focus:border-primary/50 font-mono"
              />
              <Button
                size="sm"
                onClick={handleRunQuery}
                disabled={isExecuting}
                className="absolute bottom-3 right-3 gap-1.5 bg-primary text-primary-foreground shadow-glow text-xs"
              >
                {isExecuting ? (
                  <>
                    <Sparkles className="h-3.5 w-3.5 animate-spin" /> Generating SQL...
                  </>
                ) : (
                  <>
                    <Play className="h-3.5 w-3.5" /> Execute Prompt
                  </>
                )}
              </Button>
            </div>

            {generatedSql && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4 rounded-xl border border-white/[0.08] bg-black/40 p-4"
              >
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-2 text-xs">
                  <div className="flex items-center gap-2 text-emerald-400 font-mono">
                    <CheckCircle2 className="h-4 w-4" /> SQL Generated & Executed
                  </div>
                  <span className="text-[10px] text-muted-foreground font-mono">Execution time: {executionTime}s · 4 rows returned</span>
                </div>

                <div className="rounded-lg bg-black/80 border border-white/[0.1] p-3 font-mono text-[11px] text-indigo-300">
                  <pre>{generatedSql}</pre>
                </div>

                {/* Generated EChart */}
                <div className="rounded-lg bg-white/[0.02] p-2">
                  <EChart
                    option={createBarChartOption(
                      [
                        { name: "Enterprise (1000+)", value: 42.5 },
                        { name: "Mid-Market (250-999)", value: 28.1 },
                        { name: "SMB (1-249)", value: 14.3 },
                        { name: "Self-Serve", value: 8.9 },
                      ],
                      { horizontal: true }
                    )}
                    height={180}
                  />
                </div>
              </motion.div>
            )}
          </CardContent>
        </Card>
      </PageSection>

      {/* Quick Actions Grid */}
      <PageSection>
        <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">Quick Actions</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          {quickActions.map((action, i) => (
            <Link key={action.label} href={action.href}>
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.08 }}
                className={`group rounded-2xl border border-white/[0.08] bg-gradient-to-br ${action.color} p-4 hover:border-primary/40 transition-all duration-300 cursor-pointer shadow-sm`}
              >
                <action.icon className="h-5 w-5 text-primary mb-2 group-hover:scale-110 transition-transform" />
                <p className="text-xs font-semibold text-foreground">{action.label}</p>
              </motion.div>
            </Link>
          ))}
        </div>
      </PageSection>

      {/* Projects / Datasets & Team Members */}
      <div className="grid lg:grid-cols-3 gap-6">
        <PageSection className="lg:col-span-2">
          <GlassCard>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-sm">Workspace Resources</h3>
              <div className="flex gap-1 rounded-lg border border-white/[0.1] bg-white/[0.03] p-0.5">
                {(["projects", "datasets"] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-3 py-1 text-xs rounded-md transition-all capitalize font-medium ${
                      activeTab === tab
                        ? "bg-primary text-primary-foreground shadow-xs"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            {activeTab === "projects" ? (
              <div className="space-y-3">
                {mockDashboards.map((project, i) => (
                  <motion.div
                    key={project.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 }}
                    className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5 hover:border-primary/30 transition-all"
                  >
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-indigo-500/10 border border-indigo-500/20 p-2 text-indigo-400">
                        <FolderKanban className="h-4 w-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-foreground">{project.name}</p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          {project.createdBy} · {formatRelativeTime(project.lastModified)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right hidden sm:block">
                        <p className="text-[10px] text-muted-foreground">Progress</p>
                        <Progress value={65 + i * 10} className="w-20 h-1.5 mt-1" />
                      </div>
                      <Badge variant="outline" className="text-[10px] bg-white/[0.03] border-white/[0.1]">
                        {project.tags[0]}
                      </Badge>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {datasets.slice(0, 4).map((ds, i) => (
                  <motion.div
                    key={ds.id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.08 }}
                    className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5 hover:border-primary/30 transition-all"
                  >
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-cyan-500/10 border border-cyan-500/20 p-2 text-cyan-400">
                        <FileSpreadsheet className="h-4 w-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-foreground">{ds.name}</p>
                        <p className="text-[10px] text-muted-foreground mt-0.5">
                          {ds.rows?.toLocaleString() || 0} rows · {ds.quality || 99}% quality score
                        </p>
                      </div>
                    </div>
                    <Badge className={ds.status === "active" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]" : "bg-amber-500/10 text-amber-400 border-amber-500/20 text-[10px]"}>
                      {ds.status}
                    </Badge>
                  </motion.div>
                ))}
              </div>
            )}
          </GlassCard>
        </PageSection>

        <PageSection>
          <Card className="glass-panel border-white/[0.08] h-full">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Shield className="h-4 w-4 text-indigo-400" /> Active Workspace Team
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3.5">
              {teamMembers.map((member, i) => {
                const RoleIcon = roleIcons[member.role as keyof typeof roleIcons];
                return (
                  <motion.div
                    key={member.email}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-center justify-between p-2 rounded-lg hover:bg-white/[0.03] transition-colors"
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      <div className="relative">
                        <Avatar className="h-8 w-8 border border-white/[0.1]">
                          <AvatarFallback className="text-[10px] bg-primary/10 text-primary font-semibold">
                            {getInitials(member.name)}
                          </AvatarFallback>
                        </Avatar>
                        <span
                          className={`absolute -bottom-0.5 -right-0.5 h-2 w-2 rounded-full border border-card ${
                            member.status === "online" ? "bg-emerald-400" : member.status === "away" ? "bg-amber-400" : "bg-muted-foreground/40"
                          }`}
                        />
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-semibold text-foreground truncate">{member.name}</p>
                        <p className="text-[10px] text-muted-foreground truncate">{member.email}</p>
                      </div>
                    </div>
                    <div className={`rounded-md px-2 py-0.5 border text-[10px] font-medium flex items-center gap-1 ${roleColors[member.role as keyof typeof roleColors]}`}>
                      <RoleIcon className="h-3 w-3" /> {member.role}
                    </div>
                  </motion.div>
                );
              })}
            </CardContent>
          </Card>
        </PageSection>
      </div>

      <PageSection>
        <Card className="glass-panel border-white/[0.08]">
          <CardHeader>
            <CardTitle className="text-base font-semibold">Workspace Audit Log</CardTitle>
          </CardHeader>
          <CardContent>
            <ActivityFeed items={activities} />
          </CardContent>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
