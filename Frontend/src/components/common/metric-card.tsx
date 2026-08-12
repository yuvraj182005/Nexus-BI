"use client";

import { motion } from "framer-motion";
import { LucideIcon, TrendingDown, TrendingUp, Minus } from "lucide-react";
import { cn, formatPercent } from "@/lib/utils";
import { AnimatedCounter } from "./animated-counter";

interface MetricCardProps {
  label: string;
  value: number | string;
  change?: number;
  changeType?: "increase" | "decrease" | "neutral";
  prefix?: string;
  suffix?: string;
  icon?: LucideIcon;
  className?: string;
  delay?: number;
}

export function MetricCard({
  label,
  value,
  change,
  changeType = "neutral",
  prefix,
  suffix,
  icon: Icon,
  className,
  delay = 0,
}: MetricCardProps) {
  const ChangeIcon =
    changeType === "increase"
      ? TrendingUp
      : changeType === "decrease"
        ? TrendingDown
        : Minus;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className={cn(
        "group relative overflow-hidden rounded-xl border border-border bg-card p-5 transition-all duration-300 hover:border-primary/30 hover:shadow-glow",
        className
      )}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />

      <div className="relative flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">{label}</p>
          <div className="text-2xl font-bold tracking-tight">
            {typeof value === "number" ? (
              <AnimatedCounter value={value} prefix={prefix} suffix={suffix} />
            ) : (
              <span>
                {prefix}
                {value}
                {suffix}
              </span>
            )}
          </div>
          {change !== undefined && (
            <div
              className={cn(
                "flex items-center gap-1 text-xs font-medium",
                changeType === "increase" && "text-emerald-400",
                changeType === "decrease" && "text-red-400",
                changeType === "neutral" && "text-muted-foreground"
              )}
            >
              <ChangeIcon className="h-3 w-3" />
              {formatPercent(change)}
            </div>
          )}
        </div>
        {Icon && (
          <div className="rounded-lg bg-primary/10 p-2.5">
            <Icon className="h-5 w-5 text-primary" />
          </div>
        )}
      </div>
    </motion.div>
  );
}
