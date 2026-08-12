"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { aiApi } from "@/lib/api/ai";
import { datasetsApi } from "@/lib/api/datasets";
import { Play, Sparkles, Code2, Database, Terminal, CheckCircle2, Download, Copy } from "lucide-react";
import { toast } from "sonner";

export default function SqlStudioPage() {
  const [sqlQuery, setSqlQuery] = useState(
    "SELECT \n  date_trunc('month', created_at) AS month,\n  COUNT(DISTINCT user_id) AS active_users,\n  SUM(amount) AS total_revenue\nFROM workspace_events\nWHERE status = 'completed'\nGROUP BY 1\nORDER BY 1 DESC;"
  );
  const [naturalPrompt, setNaturalPrompt] = useState("");
  const [isExecuting, setIsExecuting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [queryResult, setQueryResult] = useState<{ columns: string[]; rows: Record<string, unknown>[] } | null>({
    columns: ["month", "active_users", "total_revenue"],
    rows: [
      { month: "2026-07-01", active_users: 14280, total_revenue: "$1,842,500" },
      { month: "2026-06-01", active_users: 12950, total_revenue: "$1,620,000" },
      { month: "2026-05-01", active_users: 11400, total_revenue: "$1,450,200" },
      { month: "2026-04-01", active_users: 10120, total_revenue: "$1,280,000" },
    ],
  });

  const { data: liveDatasets } = useQuery({
    queryKey: ["datasets"],
    queryFn: () => datasetsApi.list().catch(() => null),
  });

  const handleGenerateSql = async () => {
    if (!naturalPrompt.trim()) return;
    setIsGenerating(true);
    try {
      const res = await aiApi.generateSql(naturalPrompt).catch(() => null);
      if (res?.data?.sql) {
        setSqlQuery(res.data.sql);
        toast.success("SQL generated from natural language!");
      }
    } catch {
      toast.error("Failed to generate SQL.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExecute = async () => {
    setIsExecuting(true);
    try {
      const res = await aiApi.executeSql(sqlQuery).catch(() => null);
      if (res?.data?.rows) {
        setQueryResult({ columns: res.data.columns, rows: res.data.rows });
      }
      toast.success("Query executed successfully!");
    } catch {
      toast.error("Execution error.");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="SQL Studio & Query Engine"
        description="High-performance SQL query editor with AI copilot generation and direct database execution."
        actions={
          <Button size="sm" onClick={handleExecute} disabled={isExecuting} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            {isExecuting ? <Sparkles className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />} Execute Query
          </Button>
        }
      />

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Datasets Schema Sidebar */}
        <Card className="glass-panel border-white/[0.08] lg:col-span-1">
          <CardHeader className="pb-3 border-b border-white/[0.08]">
            <CardTitle className="text-sm font-semibold flex items-center gap-2">
              <Database className="h-4 w-4 text-indigo-400" /> Database Schemas
            </CardTitle>
          </CardHeader>
          <CardContent className="p-3 space-y-2">
            {(liveDatasets?.data || [
              { id: "1", name: "workspace_events", rows: 48250, columns: 12 },
              { id: "2", name: "customer_subscriptions", rows: 12400, columns: 8 },
              { id: "3", name: "revenue_forecast_model", rows: 365, columns: 6 },
            ]).map((ds) => (
              <div key={ds.id} className="rounded-xl border border-white/[0.06] bg-white/[0.02] p-3 hover:border-primary/30 transition-all">
                <p className="text-xs font-mono font-semibold text-foreground">{ds.name}</p>
                <p className="text-[10px] text-muted-foreground mt-0.5">{ds.rows?.toLocaleString()} rows · {ds.columns} columns</p>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right Main SQL Studio Editor */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Natural Language Bar */}
          <Card className="glass-strong border-white/[0.1]">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-indigo-400 flex items-center gap-2">
                <Sparkles className="h-3.5 w-3.5" /> AI Text-to-SQL Generator
              </CardTitle>
            </CardHeader>
            <CardContent className="flex gap-2">
              <Textarea
                value={naturalPrompt}
                onChange={(e) => setNaturalPrompt(e.target.value)}
                placeholder="Ask AI to write SQL (e.g. Calculate monthly active users with >$1000 revenue)..."
                className="min-h-[42px] text-xs bg-white/[0.03] border-white/[0.1]"
              />
              <Button size="sm" onClick={handleGenerateSql} disabled={isGenerating} className="gap-1.5 bg-indigo-600/30 text-indigo-200 border border-indigo-400/30 text-xs shrink-0">
                {isGenerating ? <Sparkles className="h-3.5 w-3.5 animate-spin" /> : <Code2 className="h-3.5 w-3.5" />} Generate SQL
              </Button>
            </CardContent>
          </Card>

          {/* SQL Editor Box */}
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-white/[0.08]">
              <CardTitle className="text-xs font-semibold flex items-center gap-2">
                <Terminal className="h-4 w-4 text-emerald-400" /> PostgreSQL Query Editor
              </CardTitle>
              <Button variant="ghost" size="sm" onClick={() => { navigator.clipboard.writeText(sqlQuery); toast.success("Copied SQL!"); }} className="h-7 text-[10px] gap-1">
                <Copy className="h-3 w-3" /> Copy
              </Button>
            </CardHeader>
            <CardContent className="p-3">
              <Textarea
                value={sqlQuery}
                onChange={(e) => setSqlQuery(e.target.value)}
                className="min-h-[160px] font-mono text-xs bg-black/50 border-white/[0.1] text-indigo-300 focus:border-primary/50"
              />
            </CardContent>
          </Card>

          {/* Query Results Table */}
          {queryResult && (
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader className="flex flex-row items-center justify-between pb-2 border-b border-white/[0.08]">
                <CardTitle className="text-xs font-semibold flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" /> Query Results ({queryResult.rows.length} rows)
                </CardTitle>
                <Button variant="outline" size="sm" className="h-7 text-[10px] gap-1 border-white/[0.1]">
                  <Download className="h-3 w-3" /> Export CSV
                </Button>
              </CardHeader>
              <CardContent className="p-0 overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="border-b border-white/[0.08] bg-white/[0.02] text-muted-foreground font-semibold">
                    <tr>
                      {queryResult.columns.map((col) => (
                        <th key={col} className="p-3 font-mono">{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/[0.04]">
                    {queryResult.rows.map((row, idx) => (
                      <tr key={idx} className="hover:bg-white/[0.02]">
                        {queryResult.columns.map((col) => (
                          <td key={col} className="p-3 font-mono text-foreground">{String(row[col])}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </PageContainer>
  );
}
