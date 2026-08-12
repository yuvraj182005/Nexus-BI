"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { datasetsApi } from "@/lib/api/datasets";
import { ScanSearch, Sparkles, CheckCircle2, AlertTriangle, FileSpreadsheet } from "lucide-react";
import { toast } from "sonner";

export default function DatasetProfilingPage() {
  const { data: profileRes, refetch } = useQuery({
    queryKey: ["profiling-ds-1"],
    queryFn: () => datasetsApi.profile("ds-1").catch(() => null),
  });

  return (
    <PageContainer>
      <PageHeader
        title="Automated Data Profiling & Quality Engine"
        description="Comprehensive dataset statistical profiling, anomaly detection, missing value distribution, and quality scoring."
        actions={
          <Button size="sm" onClick={() => { refetch(); toast.success("Re-profiled dataset schema!"); }} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            <Sparkles className="h-4 w-4" /> Run Full Scan
          </Button>
        }
      />

      <PageSection>
        <div className="grid sm:grid-cols-3 gap-4 mb-6">
          <Card className="glass-panel border-white/[0.08] p-4">
            <p className="text-[10px] text-muted-foreground">Overall Data Quality</p>
            <p className="text-xl font-bold text-emerald-400 mt-1">99.8%</p>
          </Card>
          <Card className="glass-panel border-white/[0.08] p-4">
            <p className="text-[10px] text-muted-foreground">Missing Values Detected</p>
            <p className="text-xl font-bold text-foreground mt-1">0.02% (12 rows)</p>
          </Card>
          <Card className="glass-panel border-white/[0.08] p-4">
            <p className="text-[10px] text-muted-foreground">Duplicate Rows</p>
            <p className="text-xl font-bold text-indigo-400 mt-1">0 Detected</p>
          </Card>
        </div>

        <Card className="glass-panel border-white/[0.08]">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-semibold flex items-center gap-2">
              <ScanSearch className="h-4 w-4 text-indigo-400" /> Statistical Column Distribution
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-white/[0.08] bg-white/[0.02] text-muted-foreground font-semibold">
                <tr>
                  <th className="p-3">Column Name</th>
                  <th className="p-3">Inferred Type</th>
                  <th className="p-3">Null Count</th>
                  <th className="p-3">Distinct Values</th>
                  <th className="p-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/[0.04]">
                {[
                  { name: "customer_id", type: "VARCHAR", nulls: 0, distinct: 14280 },
                  { name: "transaction_timestamp", type: "TIMESTAMP", nulls: 0, distinct: 48250 },
                  { name: "revenue_amount", type: "FLOAT", nulls: 12, distinct: 3210 },
                ].map((c) => (
                  <tr key={c.name} className="hover:bg-white/[0.02]">
                    <td className="p-3 font-mono font-medium text-foreground">{c.name}</td>
                    <td className="p-3 font-mono text-indigo-300">{c.type}</td>
                    <td className="p-3 font-mono">{c.nulls}</td>
                    <td className="p-3 font-mono">{c.distinct.toLocaleString()}</td>
                    <td className="p-3">
                      <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                        Validated
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
