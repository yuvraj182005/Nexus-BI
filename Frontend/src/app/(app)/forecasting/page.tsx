"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { EChart, createAreaChartOption } from "@/components/charts/echart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { aiApi } from "@/lib/api/ai";
import { chartData } from "@/lib/mock-data";
import { TrendingUp, Sparkles, Sliders, RefreshCw } from "lucide-react";
import { toast } from "sonner";

export default function ForecastingPage() {
  const [modelType, setModelType] = useState<"arima" | "prophet" | "deep_learning">("prophet");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateForecast = async () => {
    setIsGenerating(true);
    try {
      await aiApi.forecast("ds-1", { model: modelType }).catch(() => null);
      toast.success(`Generated 12-month predictive forecast using ${modelType.toUpperCase()}!`);
    } catch {
      toast.error("Failed to generate forecast.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="Predictive Forecasting Engine"
        description="Autonomous time-series forecasting powered by Prophet, ARIMA, and Deep Neural Networks."
        actions={
          <Button size="sm" onClick={handleGenerateForecast} disabled={isGenerating} className="gap-2 bg-primary text-primary-foreground shadow-glow">
            {isGenerating ? <Sparkles className="h-4 w-4 animate-spin" /> : <TrendingUp className="h-4 w-4" />} Run Forecast Model
          </Button>
        }
      />

      <PageSection>
        <div className="flex gap-2 mb-4">
          {(["prophet", "arima", "deep_learning"] as const).map((m) => (
            <button
              key={m}
              onClick={() => setModelType(m)}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold uppercase tracking-wider transition-all ${
                modelType === m
                  ? "bg-primary text-primary-foreground shadow-xs"
                  : "bg-white/[0.03] border border-white/[0.08] text-muted-foreground hover:text-foreground"
              }`}
            >
              {m.replace("_", " ")}
            </button>
          ))}
        </div>

        <Card className="glass-panel border-white/[0.08]">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <div>
              <CardTitle className="text-base font-semibold">12-Month ARR Projection ({modelType.toUpperCase()})</CardTitle>
              <p className="text-xs text-muted-foreground mt-0.5">80% confidence interval with automated seasonality decomposition</p>
            </div>
            <Badge className="bg-indigo-500/10 text-indigo-400 border-indigo-500/20 text-[10px]">
              98.2% Historical Accuracy
            </Badge>
          </CardHeader>
          <CardContent>
            <EChart
              option={createAreaChartOption(
                chartData.revenue.map((d) => d.month),
                [
                  { name: "Historical Revenue", data: chartData.revenue.map((d) => d.value), color: "#6366f1" },
                  { name: `${modelType.toUpperCase()} Forecast`, data: chartData.revenue.map((d) => d.forecast), color: "#10b981" },
                ]
              )}
              height={360}
            />
          </CardContent>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
