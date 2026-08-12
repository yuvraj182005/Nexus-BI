"use client";

import { motion } from "framer-motion";
import {
  Brain,
  BarChart3,
  Database,
  GitBranch,
  Shield,
  Bot,
  TrendingUp,
  Terminal,
  Sparkles,
  Layers,
  Zap,
  Globe,
} from "lucide-react";

const features = [
  {
    icon: Database,
    title: "Unified Data Platform",
    description: "Connect 200+ data sources. Upload, sync, and manage datasets with automatic profiling and quality scoring.",
    color: "from-blue-500/20 to-cyan-500/20",
  },
  {
    icon: Brain,
    title: "AI-Powered Analytics",
    description: "Natural language queries, automated insights, anomaly detection, and intelligent data cleaning powered by advanced ML.",
    color: "from-purple-500/20 to-pink-500/20",
  },
  {
    icon: BarChart3,
    title: "Interactive Dashboards",
    description: "Build stunning dashboards with drag-and-drop. Real-time updates, cross-filtering, and embedded analytics.",
    color: "from-indigo-500/20 to-violet-500/20",
  },
  {
    icon: TrendingUp,
    title: "Advanced Forecasting",
    description: "Prophet, ARIMA, and neural forecasting models with confidence intervals and scenario planning.",
    color: "from-emerald-500/20 to-teal-500/20",
  },
  {
    icon: Terminal,
    title: "SQL Intelligence",
    description: "Generate, optimize, and explain SQL from natural language. Semantic layer with auto-join suggestions.",
    color: "from-amber-500/20 to-orange-500/20",
  },
  {
    icon: Bot,
    title: "AI Agents & Copilot",
    description: "Autonomous AI agents for data tasks. Copilot assists with analysis, reporting, and workflow automation.",
    color: "from-rose-500/20 to-red-500/20",
  },
  {
    icon: GitBranch,
    title: "Workflow Automation",
    description: "Visual workflow builder with triggers, conditions, and actions. Schedule ETL, reports, and alerts.",
    color: "from-sky-500/20 to-blue-500/20",
  },
  {
    icon: Shield,
    title: "Enterprise Governance",
    description: "Row-level security, data lineage, audit trails, compliance frameworks, and role-based access control.",
    color: "from-slate-500/20 to-zinc-500/20",
  },
];

export function FeaturesSection() {
  return (
    <section id="features" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-1.5 text-sm text-primary mb-4">
            <Sparkles className="h-3.5 w-3.5" />
            Platform Capabilities
          </div>
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Everything you need to{" "}
            <span className="gradient-text">decide smarter</span>
          </h2>
          <p className="mt-4 text-muted-foreground max-w-2xl mx-auto text-lg">
            From raw data to actionable insights — a complete intelligence stack
            designed for enterprise teams.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="group relative rounded-xl border border-border bg-card p-6 transition-all duration-300 hover:border-primary/30 hover:shadow-glow"
            >
              <div className={`absolute inset-0 rounded-xl bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`} />
              <div className="relative">
                <div className="rounded-lg bg-primary/10 w-fit p-2.5 mb-4">
                  <feature.icon className="h-5 w-5 text-primary" />
                </div>
                <h3 className="font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function ArchitectureSection() {
  const layers = [
    { icon: Globe, label: "Presentation", items: ["Dashboards", "Reports", "Embedded Analytics"] },
    { icon: Bot, label: "AI Layer", items: ["Copilot", "Agents", "NL to SQL", "Forecasting"] },
    { icon: Layers, label: "Semantic Layer", items: ["Models", "Metrics", "Dimensions", "Relationships"] },
    { icon: Zap, label: "Processing", items: ["ETL", "Streaming", "ML Pipeline", "Quality"] },
    { icon: Database, label: "Data Layer", items: ["Warehouses", "Lakes", "APIs", "Files"] },
  ];

  return (
    <section id="architecture" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Unified <span className="gradient-text">Architecture</span>
          </h2>
          <p className="mt-4 text-muted-foreground max-w-2xl mx-auto text-lg">
            A modern data stack built as one cohesive platform, not stitched-together tools.
          </p>
        </motion.div>

        <div className="space-y-3 max-w-3xl mx-auto">
          {layers.map((layer, i) => (
            <motion.div
              key={layer.label}
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="flex items-center gap-4 rounded-xl border border-border bg-card/50 p-4 backdrop-blur-sm hover:border-primary/20 transition-colors"
            >
              <div className="rounded-lg bg-primary/10 p-2.5 shrink-0">
                <layer.icon className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-sm">{layer.label}</h3>
                <div className="flex flex-wrap gap-2 mt-1.5">
                  {layer.items.map((item) => (
                    <span key={item} className="text-xs text-muted-foreground bg-secondary/50 rounded-md px-2 py-0.5">
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
