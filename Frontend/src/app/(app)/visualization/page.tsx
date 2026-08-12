"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { EChart, createAreaChartOption, createBarChartOption, createPieChartOption } from "@/components/charts/echart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { chartData } from "@/lib/mock-data";
import { PieChart, BarChart3, LineChart } from "lucide-react";

export default function VisualizationStudioPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Visualization Studio & Chart Specs"
        description="Interactive chart builder powered by ECharts with custom color palettes and responsive canvas bounds."
      />

      <div className="grid lg:grid-cols-2 gap-6">
        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <LineChart className="h-4 w-4 text-indigo-400" /> Area Gradient Specification
              </CardTitle>
            </CardHeader>
            <CardContent>
              <EChart
                option={createAreaChartOption(
                  chartData.revenue.map((d) => d.month),
                  [{ name: "Revenue", data: chartData.revenue.map((d) => d.value), color: "#6366f1" }]
                )}
                height={260}
              />
            </CardContent>
          </Card>
        </PageSection>

        <PageSection>
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <PieChart className="h-4 w-4 text-emerald-400" /> Donut Ratio Specs
              </CardTitle>
            </CardHeader>
            <CardContent>
              <EChart option={createPieChartOption(chartData.categories, { donut: true })} height={260} />
            </CardContent>
          </Card>
        </PageSection>

        <PageSection className="lg:col-span-2">
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-cyan-400" /> Horizontal Bar Ranking
              </CardTitle>
            </CardHeader>
            <CardContent>
              <EChart
                option={createBarChartOption(
                  [
                    { name: "PostgreSQL Production DB", value: 98.4 },
                    { name: "Snowflake Analytics Warehouse", value: 89.2 },
                    { name: "BigQuery Customer Stream", value: 74.1 },
                    { name: "Amazon S3 Data Lake", value: 62.8 },
                  ],
                  { horizontal: true }
                )}
                height={240}
              />
            </CardContent>
          </Card>
        </PageSection>
      </div>
    </PageContainer>
  );
}
