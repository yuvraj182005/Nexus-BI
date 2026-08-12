"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PageContainer, PageHeader } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { getInitials } from "@/lib/utils";
import {
  Settings,
  User,
  Shield,
  Key,
  Users,
  CreditCard,
  Building2,
  Copy,
  Check,
  Plus,
  Crown,
  Lock,
  Globe,
  BellRing,
  Sparkles,
} from "lucide-react";

import { useQuery } from "@tanstack/react-query";
import { authApi } from "@/lib/api/auth";

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<"general" | "profile" | "security" | "team" | "billing">("general");
  const [copiedKey, setCopiedKey] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  const { data: currentUser } = useQuery({
    queryKey: ["current-user"],
    queryFn: () => authApi.me().catch(() => null),
  });

  const user = currentUser?.data || {
    name: "K Bhramee Sundaram",
    email: "bhramee@nexusbi.ai",
    role: "admin",
    organization: "NexusBI Enterprise",
  };

  const handleCopyKey = () => {
    navigator.clipboard.writeText("nexus_live_sk_894029140921849182390");
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
  };

  const handleSave = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  return (
    <PageContainer>
      <PageHeader
        title="Workspace & System Settings"
        description="Manage workspace organization, security policies, API keys, team roles, and enterprise billing."
      />

      {/* Tab Selector Header */}
      <div className="flex flex-wrap gap-2 border-b border-white/[0.08] pb-4 mb-6">
        {[
          { id: "general", label: "General", icon: Building2 },
          { id: "profile", label: "Profile", icon: User },
          { id: "security", label: "Security & API Keys", icon: Key },
          { id: "team", label: "Team Members", icon: Users },
          { id: "billing", label: "Usage & Billing", icon: CreditCard },
        ].map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-semibold transition-all duration-200 ${
                isActive
                  ? "glass-strong border-primary/40 text-primary shadow-glow"
                  : "text-muted-foreground hover:text-foreground hover:bg-white/[0.03]"
              }`}
            >
              <Icon className={`h-4 w-4 ${isActive ? "text-primary" : "text-muted-foreground"}`} />
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab Panels */}
      <AnimatePresence mode="wait">
        {activeTab === "general" && (
          <motion.div
            key="general"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader>
                <CardTitle className="text-base font-semibold">Workspace Profile</CardTitle>
                <CardDescription className="text-xs">Primary identification and regional preferences</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 max-w-xl">
                <div className="space-y-1.5">
                  <Label className="text-xs">Workspace Name</Label>
                  <Input defaultValue="Production BI Cluster" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs">Workspace Slug / Subdomain</Label>
                  <div className="flex items-center gap-2">
                    <Input defaultValue="production-bi" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                    <span className="text-xs text-muted-foreground font-mono">.nexusbi.ai</span>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs">Default Region</Label>
                    <Input defaultValue="us-east-1 (N. Virginia)" readOnly className="bg-white/[0.02] border-white/[0.08] text-xs font-mono text-muted-foreground" />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs">Primary Currency</Label>
                    <Input defaultValue="USD ($)" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                  </div>
                </div>
                <div className="pt-2">
                  <Button onClick={handleSave} className="bg-primary text-primary-foreground shadow-glow text-xs gap-2">
                    {savedSuccess ? <Check className="h-4 w-4 text-emerald-400" /> : null}
                    {savedSuccess ? "Saved Changes!" : "Save Workspace Settings"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === "profile" && (
          <motion.div
            key="profile"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader>
                <CardTitle className="text-base font-semibold">User Account Details</CardTitle>
                <CardDescription className="text-xs">Manage personal details and notifications</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4 max-w-xl">
                <div className="flex items-center gap-4 border-b border-white/[0.08] pb-4">
                  <Avatar className="h-14 w-14 border border-indigo-400/40">
                    <AvatarFallback className="bg-gradient-to-br from-indigo-500/30 to-purple-500/30 text-indigo-200 text-base font-bold">
                      KB
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <Button variant="outline" size="sm" className="text-xs border-white/[0.1] bg-white/[0.03]">
                      Change Avatar
                    </Button>
                    <p className="text-[10px] text-muted-foreground mt-1">JPG, PNG or GIF. Max 2MB.</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <Label className="text-xs">Full Name</Label>
                    <Input defaultValue="K Bhramee Sundaram" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                  </div>
                  <div className="space-y-1.5">
                    <Label className="text-xs">Job Title</Label>
                    <Input defaultValue="VP of Analytics & AI" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs">Email Address</Label>
                  <Input defaultValue="bhramee@nexusbi.ai" className="bg-white/[0.03] border-white/[0.1] text-xs" />
                </div>
                <div className="pt-2">
                  <Button onClick={handleSave} className="bg-primary text-primary-foreground shadow-glow text-xs gap-2">
                    {savedSuccess ? <Check className="h-4 w-4 text-emerald-400" /> : null}
                    {savedSuccess ? "Saved Profile!" : "Save Profile Details"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === "security" && (
          <motion.div
            key="security"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-base font-semibold flex items-center gap-2">
                    <Key className="h-4 w-4 text-indigo-400" /> Workspace API Secret Keys
                  </CardTitle>
                  <CardDescription className="text-xs">Authenticate Python SDK, REST API, or CLI pipelines</CardDescription>
                </div>
                <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground text-xs shadow-glow">
                  <Plus className="h-3.5 w-3.5" /> Generate New Key
                </Button>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-xl border border-white/[0.08] bg-black/40 p-3.5 flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="text-xs font-semibold text-foreground">Production System Key</p>
                      <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[9px]">Active</Badge>
                    </div>
                    <p className="text-[11px] font-mono text-muted-foreground mt-1">nexus_live_sk_894029140921849182390</p>
                  </div>
                  <Button variant="outline" size="sm" onClick={handleCopyKey} className="gap-1.5 text-xs border-white/[0.1]">
                    {copiedKey ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                    {copiedKey ? "Copied" : "Copy Secret"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === "team" && (
          <motion.div
            key="team"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-base font-semibold">Workspace Member Access</CardTitle>
                  <CardDescription className="text-xs">Role-based access control and seat management</CardDescription>
                </div>
                <Button size="sm" className="gap-1.5 bg-primary text-primary-foreground text-xs shadow-glow">
                  <Plus className="h-3.5 w-3.5" /> Invite Member
                </Button>
              </CardHeader>
              <CardContent className="p-0 overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="border-b border-white/[0.08] bg-white/[0.02] text-muted-foreground font-semibold">
                    <tr>
                      <th className="p-3.5">Member</th>
                      <th className="p-3.5">Role</th>
                      <th className="p-3.5">Status</th>
                      <th className="p-3.5 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/[0.04]">
                    {[
                      { name: "K Bhramee Sundaram", email: "bhramee@nexusbi.ai", role: "Owner", status: "Active" },
                      { name: "Sarah Chen", email: "sarah@nexusbi.ai", role: "Admin", status: "Active" },
                      { name: "Marcus Johnson", email: "marcus@nexusbi.ai", role: "Analyst", status: "Active" },
                    ].map((m, idx) => (
                      <tr key={idx} className="hover:bg-white/[0.02] transition-colors">
                        <td className="p-3.5">
                          <div className="flex items-center gap-2.5">
                            <Avatar className="h-7 w-7 border border-white/[0.1]">
                              <AvatarFallback className="text-[10px] bg-primary/10 text-primary">
                                {getInitials(m.name)}
                              </AvatarFallback>
                            </Avatar>
                            <div>
                              <p className="font-semibold text-foreground">{m.name}</p>
                              <p className="text-[10px] text-muted-foreground">{m.email}</p>
                            </div>
                          </div>
                        </td>
                        <td className="p-3.5">
                          <Badge variant="outline" className="border-indigo-500/30 bg-indigo-500/10 text-indigo-300 text-[10px]">
                            {m.role}
                          </Badge>
                        </td>
                        <td className="p-3.5">
                          <span className="text-emerald-400 font-medium">{m.status}</span>
                        </td>
                        <td className="p-3.5 text-right">
                          <Button variant="ghost" size="sm" className="text-xs text-muted-foreground hover:text-foreground">
                            Edit Role
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {activeTab === "billing" && (
          <motion.div
            key="billing"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="space-y-6"
          >
            <Card className="glass-panel border-white/[0.08]">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <CardTitle className="text-base font-semibold">Active Enterprise Plan</CardTitle>
                    <Badge className="bg-indigo-500/20 text-indigo-300 border-indigo-500/30 text-[10px] gap-1">
                      <Crown className="h-3 w-3 text-amber-400" /> Enterprise Pro
                    </Badge>
                  </div>
                  <CardDescription className="text-xs mt-0.5">Billed annually · Next cycle Sep 1, 2026</CardDescription>
                </div>
                <Button variant="outline" size="sm" className="text-xs border-white/[0.1]">
                  Manage Subscription
                </Button>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid sm:grid-cols-3 gap-4">
                  <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                    <p className="text-[10px] text-muted-foreground font-medium">Data Warehouse Storage</p>
                    <p className="text-lg font-bold text-foreground mt-1">4.2 TB / 10 TB</p>
                    <Progress value={42} className="h-1.5 mt-2 bg-white/[0.05]" />
                  </div>
                  <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                    <p className="text-[10px] text-muted-foreground font-medium">AI Reasoning Credits</p>
                    <p className="text-lg font-bold text-foreground mt-1">84,200 / 100,000</p>
                    <Progress value={84} className="h-1.5 mt-2 bg-white/[0.05]" />
                  </div>
                  <div className="rounded-xl border border-white/[0.08] bg-white/[0.02] p-4">
                    <p className="text-[10px] text-muted-foreground font-medium">Active User Seats</p>
                    <p className="text-lg font-bold text-foreground mt-1">12 / Unlimited</p>
                    <Progress value={20} className="h-1.5 mt-2 bg-white/[0.05]" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </PageContainer>
  );
}
