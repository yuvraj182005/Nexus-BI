"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import type { Dataset } from "@/types";
import { formatBytes, formatRelativeTime } from "@/lib/utils";
import { Database, FileSpreadsheet, Braces, Server, Globe } from "lucide-react";

const typeIcons = {
  csv: FileSpreadsheet,
  json: Braces,
  parquet: Database,
  sql: Server,
  api: Globe,
};

const statusVariants = {
  active: "success" as const,
  processing: "warning" as const,
  error: "destructive" as const,
  archived: "secondary" as const,
};

interface DatasetCardProps {
  dataset: Dataset;
  onClick?: () => void;
  delay?: number;
}

export function DatasetCard({ dataset, onClick, delay = 0 }: DatasetCardProps) {
  const Icon = typeIcons[dataset.type];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      onClick={onClick}
      className={cn(
        "group cursor-pointer rounded-xl border border-border bg-card p-5 transition-all duration-300 hover:border-primary/30 hover:shadow-glow",
        onClick && "cursor-pointer"
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-primary/10 p-2.5">
            <Icon className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h3 className="font-semibold group-hover:text-primary transition-colors">
              {dataset.name}
            </h3>
            <p className="text-xs text-muted-foreground mt-0.5">
              {dataset.description}
            </p>
          </div>
        </div>
        <Badge variant={statusVariants[dataset.status]}>
          {dataset.status}
        </Badge>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        <div>
          <p className="text-muted-foreground text-xs">Rows</p>
          <p className="font-medium">{dataset.rows.toLocaleString()}</p>
        </div>
        <div>
          <p className="text-muted-foreground text-xs">Columns</p>
          <p className="font-medium">{dataset.columns}</p>
        </div>
        <div>
          <p className="text-muted-foreground text-xs">Size</p>
          <p className="font-medium">{formatBytes(dataset.size)}</p>
        </div>
      </div>

      <div className="mt-4">
        <div className="flex items-center justify-between text-xs mb-1.5">
          <span className="text-muted-foreground">Data Quality</span>
          <span className="font-medium">{dataset.quality}%</span>
        </div>
        <Progress value={dataset.quality} className="h-1.5" />
      </div>

      <div className="mt-3 flex items-center justify-between">
        <div className="flex gap-1.5">
          {dataset.tags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="outline" className="text-[10px] px-1.5 py-0">
              {tag}
            </Badge>
          ))}
        </div>
        <span className="text-xs text-muted-foreground">
          {formatRelativeTime(dataset.lastUpdated)}
        </span>
      </div>
    </motion.div>
  );
}
