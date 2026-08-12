"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Hexagon, ArrowRight, Play, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { AnimatedBackground } from "@/components/common/animated-background";
import { AnimatedCounter } from "@/components/common/animated-counter";
import { EChart, createLineChartOption, createAreaChartOption } from "@/components/charts/echart";
import { APP_NAME, ROUTES } from "@/lib/constants";
import { chartData } from "@/lib/mock-data";

export function LandingHero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      <AnimatedBackground variant="landing" />

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-1.5 text-sm text-primary mb-6"
            >
              <Sparkles className="h-3.5 w-3.5" />
              Enterprise Decision Intelligence
            </motion.div>

            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1]">
              One Intelligent Platform for{" "}
              <span className="gradient-text">Data & Decisions</span>
            </h1>

            <p className="mt-6 text-lg text-muted-foreground max-w-xl leading-relaxed">
              Unify AI, analytics, data engineering, and business intelligence.
              Connect sources, build semantic models, forecast trends, and govern
              enterprise data — all in one platform.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <Link href={ROUTES.register}>
                <Button size="lg" variant="glow" className="gap-2">
                  Start Free Trial <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Button size="lg" variant="glass" className="gap-2">
                <Play className="h-4 w-4" /> Watch Demo
              </Button>
            </div>

            <div className="mt-12 grid grid-cols-3 gap-8">
              {[
                { label: "Enterprise Users", value: 50000, suffix: "+" },
                { label: "Data Processed", value: 10, suffix: " PB" },
                { label: "Uptime SLA", value: 99.99, suffix: "%", decimals: 2 },
              ].map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + i * 0.1 }}
                >
                  <div className="text-2xl md:text-3xl font-bold">
                    <AnimatedCounter
                      value={stat.value}
                      suffix={stat.suffix}
                      decimals={stat.decimals || 0}
                    />
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">{stat.label}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="relative"
          >
            <div className="glass-strong rounded-2xl p-1 shadow-glow-lg">
              <div className="rounded-xl bg-card/80 p-4 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Hexagon className="h-5 w-5 text-primary" />
                    <span className="text-sm font-semibold">Executive Dashboard</span>
                  </div>
                  <div className="flex gap-1.5">
                    <div className="h-2.5 w-2.5 rounded-full bg-red-400/60" />
                    <div className="h-2.5 w-2.5 rounded-full bg-yellow-400/60" />
                    <div className="h-2.5 w-2.5 rounded-full bg-green-400/60" />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: "Revenue", value: "$2.8M", change: "+12.5%" },
                    { label: "Users", value: "48.3K", change: "+8.2%" },
                    { label: "Conversion", value: "3.24%", change: "+2.1%" },
                    { label: "NPS Score", value: "72", change: "+5.0%" },
                  ].map((m) => (
                    <div key={m.label} className="rounded-lg bg-secondary/50 p-3">
                      <p className="text-[10px] text-muted-foreground">{m.label}</p>
                      <p className="text-lg font-bold">{m.value}</p>
                      <p className="text-[10px] text-emerald-400">{m.change}</p>
                    </div>
                  ))}
                </div>

                <EChart
                  option={createLineChartOption(
                    chartData.revenue.map((d) => ({ name: d.month, value: d.value })),
                    { area: true }
                  )}
                  height={180}
                />
              </div>
            </div>

            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
              className="absolute -top-4 -right-4 glass rounded-xl p-3 shadow-glow"
            >
              <p className="text-[10px] text-muted-foreground">AI Insight</p>
              <p className="text-xs font-medium">Revenue up 12.5% QoQ</p>
            </motion.div>

            <motion.div
              animate={{ y: [0, 8, 0] }}
              transition={{ duration: 5, repeat: Infinity }}
              className="absolute -bottom-4 -left-4 glass rounded-xl p-3 shadow-glow"
            >
              <p className="text-[10px] text-muted-foreground">Forecast</p>
              <p className="text-xs font-medium text-emerald-400">94.2% accuracy</p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
