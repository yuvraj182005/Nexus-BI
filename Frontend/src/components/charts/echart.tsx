"use client";

import dynamic from "next/dynamic";
import { Skeleton } from "@/components/ui/skeleton";

const ReactECharts = dynamic(() => import("echarts-for-react"), {
  ssr: false,
  loading: () => <Skeleton className="h-full w-full min-h-[300px]" />,
});

interface EChartProps {
  option: Record<string, unknown>;
  height?: string | number;
  className?: string;
}

export function EChart({ option, height = 300, className }: EChartProps) {
  return (
    <div className={className} style={{ height }}>
      <ReactECharts
        option={option}
        style={{ height: "100%", width: "100%" }}
        opts={{ renderer: "canvas" }}
      />
    </div>
  );
}

export function createLineChartOption(
  data: { name: string; value: number }[],
  options?: { color?: string; area?: boolean; title?: string }
) {
  return {
    backgroundColor: "transparent",
    grid: { top: 30, right: 20, bottom: 30, left: 50 },
    tooltip: {
      trigger: "axis",
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      borderColor: "rgba(99, 102, 241, 0.3)",
      textStyle: { color: "#e2e8f0" },
    },
    xAxis: {
      type: "category",
      data: data.map((d) => d.name),
      axisLine: { lineStyle: { color: "rgba(148, 163, 184, 0.2)" } },
      axisLabel: { color: "#94a3b8" },
    },
    yAxis: {
      type: "value",
      axisLine: { show: false },
      splitLine: { lineStyle: { color: "rgba(148, 163, 184, 0.1)" } },
      axisLabel: { color: "#94a3b8" },
    },
    series: [
      {
        data: data.map((d) => d.value),
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 6,
        lineStyle: { width: 2, color: options?.color || "#6366f1" },
        itemStyle: { color: options?.color || "#6366f1" },
        areaStyle: options?.area
          ? {
              color: {
                type: "linear",
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: "rgba(99, 102, 241, 0.3)" },
                  { offset: 1, color: "rgba(99, 102, 241, 0)" },
                ],
              },
            }
          : undefined,
        animationDuration: 1500,
        animationEasing: "cubicOut",
      },
    ],
  };
}

export function createBarChartOption(
  data: { name: string; value: number }[],
  options?: { color?: string; horizontal?: boolean }
) {
  const axisConfig = options?.horizontal
    ? {
        xAxis: { type: "value", axisLabel: { color: "#94a3b8" }, splitLine: { lineStyle: { color: "rgba(148, 163, 184, 0.1)" } } },
        yAxis: { type: "category", data: data.map((d) => d.name), axisLabel: { color: "#94a3b8" } },
      }
    : {
        xAxis: { type: "category", data: data.map((d) => d.name), axisLabel: { color: "#94a3b8" } },
        yAxis: { type: "value", axisLabel: { color: "#94a3b8" }, splitLine: { lineStyle: { color: "rgba(148, 163, 184, 0.1)" } } },
      };

  return {
    backgroundColor: "transparent",
    grid: { top: 20, right: 20, bottom: 30, left: 50 },
    tooltip: {
      trigger: "axis",
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      borderColor: "rgba(99, 102, 241, 0.3)",
      textStyle: { color: "#e2e8f0" },
    },
    ...axisConfig,
    series: [
      {
        data: data.map((d) => d.value),
        type: "bar",
        barWidth: "60%",
        itemStyle: {
          color: {
            type: "linear",
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: options?.color || "#818cf8" },
              { offset: 1, color: options?.color || "#6366f1" },
            ],
          },
          borderRadius: [4, 4, 0, 0],
        },
        animationDuration: 1200,
        animationEasing: "elasticOut",
      },
    ],
  };
}

export function createPieChartOption(
  data: { name: string; value: number }[],
  options?: { donut?: boolean }
) {
  return {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      borderColor: "rgba(99, 102, 241, 0.3)",
      textStyle: { color: "#e2e8f0" },
    },
    legend: {
      orient: "vertical",
      right: 10,
      top: "center",
      textStyle: { color: "#94a3b8" },
    },
    series: [
      {
        type: "pie",
        radius: options?.donut ? ["45%", "70%"] : "70%",
        center: ["40%", "50%"],
        data: data.map((d, i) => ({
          ...d,
          itemStyle: {
            color: ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe"][i % 5],
          },
        })),
        label: { color: "#94a3b8" },
        animationType: "scale",
        animationDuration: 1200,
      },
    ],
  };
}

export function createAreaChartOption(
  categories: string[],
  series: { name: string; data: number[]; color?: string }[]
) {
  return {
    backgroundColor: "transparent",
    grid: { top: 40, right: 20, bottom: 30, left: 50 },
    tooltip: {
      trigger: "axis",
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      borderColor: "rgba(99, 102, 241, 0.3)",
      textStyle: { color: "#e2e8f0" },
    },
    legend: {
      data: series.map((s) => s.name),
      textStyle: { color: "#94a3b8" },
      top: 0,
    },
    xAxis: {
      type: "category",
      data: categories,
      axisLabel: { color: "#94a3b8" },
      axisLine: { lineStyle: { color: "rgba(148, 163, 184, 0.2)" } },
    },
    yAxis: {
      type: "value",
      axisLabel: { color: "#94a3b8" },
      splitLine: { lineStyle: { color: "rgba(148, 163, 184, 0.1)" } },
    },
    series: series.map((s) => ({
      name: s.name,
      type: "line",
      smooth: true,
      data: s.data,
      lineStyle: { color: s.color || "#6366f1" },
      itemStyle: { color: s.color || "#6366f1" },
      areaStyle: {
        color: {
          type: "linear",
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: `${s.color || "#6366f1"}40` },
            { offset: 1, color: `${s.color || "#6366f1"}00` },
          ],
        },
      },
    })),
  };
}
