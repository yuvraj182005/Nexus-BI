"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { GlassCard } from "@/components/common/glass-card";
import { MetricCard } from "@/components/common/metric-card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { mockPlugins } from "@/lib/mock-data";
import {
  Puzzle,
  Settings,
  RefreshCw,
  Trash2,
  AlertCircle,
  CheckCircle2,
  ArrowUpCircle,
} from "lucide-react";

interface PluginSettings {
  autoUpdate: boolean;
  enabled: boolean;
}

export default function PluginsPage() {
  const installed = mockPlugins.filter((p) => p.installed);
  const [settings, setSettings] = useState<Record<string, PluginSettings>>(
    Object.fromEntries(installed.map((p) => [p.id, { autoUpdate: true, enabled: true }]))
  );
  const [updating, setUpdating] = useState<string | null>(null);

  const handleUpdate = async (id: string) => {
    setUpdating(id);
    await new Promise((r) => setTimeout(r, 1500));
    setUpdating(null);
  };

  const toggleSetting = (id: string, key: keyof PluginSettings) => {
    setSettings((prev) => ({
      ...prev,
      [id]: { ...prev[id], [key]: !prev[id][key] },
    }));
  };

  return (
    <PageContainer>
      <PageHeader
        title="Installed Plugins"
        description="Manage your installed plugins, configure settings, and check for updates."
        actions={
          <Button variant="outline" size="sm" className="gap-1.5">
            <RefreshCw className="h-3.5 w-3.5" /> Check All Updates
          </Button>
        }
      />

      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <MetricCard label="Installed" value={installed.length} icon={Puzzle} />
          <MetricCard label="Active" value={Object.values(settings).filter((s) => s.enabled).length} icon={CheckCircle2} change={100} changeType="increase" delay={0.1} />
          <MetricCard label="Updates Available" value={1} icon={ArrowUpCircle} delay={0.2} />
        </div>
      </PageSection>

      <PageSection>
        <Tabs defaultValue="installed">
          <TabsList>
            <TabsTrigger value="installed">Installed ({installed.length})</TabsTrigger>
            <TabsTrigger value="updates">Updates (1)</TabsTrigger>
          </TabsList>

          <TabsContent value="installed" className="mt-4 space-y-4">
            {installed.map((plugin, i) => (
              <motion.div
                key={plugin.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Card>
                  <CardHeader className="flex flex-row items-start justify-between pb-2">
                    <div className="flex items-start gap-3">
                      <div className="rounded-lg bg-primary/10 p-2.5">
                        <Puzzle className="h-5 w-5 text-primary" />
                      </div>
                      <div>
                        <CardTitle className="text-base">{plugin.name}</CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{plugin.description}</p>
                        <div className="flex items-center gap-2 mt-2">
                          <Badge variant="outline">v{plugin.version}</Badge>
                          <Badge variant="secondary">{plugin.category}</Badge>
                          {settings[plugin.id]?.enabled ? (
                            <Badge variant="success">Active</Badge>
                          ) : (
                            <Badge variant="warning">Disabled</Badge>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Settings className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-destructive hover:text-destructive">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap items-center gap-6 pt-2 border-t border-border">
                      <div className="flex items-center gap-2">
                        <Switch
                          id={`enabled-${plugin.id}`}
                          checked={settings[plugin.id]?.enabled ?? true}
                          onCheckedChange={() => toggleSetting(plugin.id, "enabled")}
                        />
                        <Label htmlFor={`enabled-${plugin.id}`} className="text-sm">Enabled</Label>
                      </div>
                      <div className="flex items-center gap-2">
                        <Switch
                          id={`auto-${plugin.id}`}
                          checked={settings[plugin.id]?.autoUpdate ?? true}
                          onCheckedChange={() => toggleSetting(plugin.id, "autoUpdate")}
                        />
                        <Label htmlFor={`auto-${plugin.id}`} className="text-sm">Auto-update</Label>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        className="gap-1.5 ml-auto"
                        disabled={updating === plugin.id}
                        onClick={() => handleUpdate(plugin.id)}
                      >
                        <RefreshCw className={`h-3.5 w-3.5 ${updating === plugin.id ? "animate-spin" : ""}`} />
                        {updating === plugin.id ? "Updating..." : "Check Update"}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </TabsContent>

          <TabsContent value="updates" className="mt-4">
            <GlassCard>
              <div className="flex items-start gap-4">
                <div className="rounded-lg bg-amber-500/10 p-2.5">
                  <AlertCircle className="h-5 w-5 text-amber-400" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold">Advanced Forecasting v1.9.0</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    New Prophet model improvements and bug fixes for seasonal decomposition.
                  </p>
                  <div className="flex items-center gap-2 mt-3">
                    <Badge variant="warning">v1.8.0 → v1.9.0</Badge>
                    <Button size="sm" className="gap-1.5">
                      <ArrowUpCircle className="h-3.5 w-3.5" /> Update Now
                    </Button>
                  </div>
                </div>
              </div>
            </GlassCard>
          </TabsContent>
        </Tabs>
      </PageSection>
    </PageContainer>
  );
}
