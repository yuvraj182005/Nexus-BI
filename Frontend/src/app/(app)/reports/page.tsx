"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Plus, Clock, Sparkles } from "lucide-react";
import { toast } from "sonner";

export default function ReportsPage() {
  const reports = [
    { id: "rep-1", title: "Q3 Enterprise Executive Summary", date: "2026-08-01", type: "PDF", size: "2.4 MB" },
    { id: "rep-2", title: "Monthly Churn Variance Analysis", date: "2026-07-28", type: "XLSX", size: "1.8 MB" },
    { id: "rep-3", title: "Data Governance & Audit Export", date: "2026-07-15", type: "CSV", size: "850 KB" },
  ];

  return (
    <PageContainer>
      <PageHeader
        title="Enterprise Reports & Export Hub"
        description="Automated PDF, Excel, and CSV executive report generation and scheduled email delivery."
        actions={
          <Button size="sm" onClick={() => toast.success("Generating new executive report...")} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            <Plus className="h-4 w-4" /> Generate New Report
          </Button>
        }
      />

      <PageSection>
        <div className="space-y-3">
          {reports.map((r) => (
            <Card key={r.id} className="glass-panel border-white/[0.08] hover:border-primary/40 transition-all p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                  <FileText className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-xs font-semibold text-foreground">{r.title}</p>
                  <p className="text-[10px] text-muted-foreground mt-0.5">{r.date} · {r.size}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Badge variant="outline" className="text-[10px] bg-white/[0.03] border-white/[0.1] font-mono">
                  {r.type}
                </Badge>
                <Button size="sm" variant="outline" onClick={() => toast.success(`Downloading ${r.title}...`)} className="gap-1.5 border-white/[0.12] text-xs">
                  <Download className="h-3.5 w-3.5" /> Download
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
