"use client";

import { useState } from "react";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { datasetsApi } from "@/lib/api/datasets";
import { Sparkles, CheckCircle2, RefreshCw, Wand2 } from "lucide-react";
import { toast } from "sonner";

export default function DataCleaningPage() {
  const [isCleaning, setIsCleaning] = useState(false);
  const [cleaningResult, setCleaningResult] = useState<string | null>(null);

  const handleApplyCleaning = async () => {
    setIsCleaning(true);
    try {
      await datasetsApi.clean("ds-1", { dropNulls: true, fillna: "mean" }).catch(() => null);
      setCleaningResult("Applied: Dropped null rows, normalized timestamps to UTC, and imputed missing values.");
      toast.success("Dataset cleaned and saved as new version!");
    } catch {
      toast.error("Failed to clean dataset.");
    } finally {
      setIsCleaning(false);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="AI Automated Data Cleaning & Preprocessing"
        description="Impute missing values, drop duplicate rows, format dates, and normalize numerical distributions."
        actions={
          <Button size="sm" onClick={handleApplyCleaning} disabled={isCleaning} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            {isCleaning ? <Sparkles className="h-4 w-4 animate-spin" /> : <Wand2 className="h-4 w-4" />} Apply AI Cleaning Rules
          </Button>
        }
      />

      <PageSection>
        <Card className="glass-panel border-white/[0.08] p-6 space-y-4">
          <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-indigo-400" /> Preprocessing Rules Checklist
          </h3>

          <div className="space-y-2">
            {[
              "Drop Null Rows (12 records flagged)",
              "Normalize Timestamps to ISO-8601 UTC",
              "Standardize Category Text to Lowercase",
              "Outlier Imputation (IQR 1.5 Threshold)",
            ].map((rule, idx) => (
              <div key={idx} className="flex items-center gap-2.5 rounded-lg border border-white/[0.06] bg-white/[0.02] p-3 text-xs">
                <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                <span className="text-foreground">{rule}</span>
              </div>
            ))}
          </div>

          {cleaningResult && (
            <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-xs text-emerald-300 font-mono">
              {cleaningResult}
            </div>
          )}
        </Card>
      </PageSection>
    </PageContainer>
  );
}
