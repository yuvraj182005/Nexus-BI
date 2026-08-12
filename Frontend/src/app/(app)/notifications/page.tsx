"use client";

import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { GlassCard } from "@/components/common/glass-card";
import { MetricCard } from "@/components/common/metric-card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { mockNotifications } from "@/lib/mock-data";
import { formatRelativeTime } from "@/lib/utils";
import type { Notification } from "@/types";
import {
  Bell,
  CheckCheck,
  Filter,
  Info,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ExternalLink,
} from "lucide-react";
import Link from "next/link";

const typeConfig = {
  info: { icon: Info, badge: "info" as const, color: "text-blue-400" },
  success: { icon: CheckCircle2, badge: "success" as const, color: "text-emerald-400" },
  warning: { icon: AlertTriangle, badge: "warning" as const, color: "text-amber-400" },
  error: { icon: XCircle, badge: "destructive" as const, color: "text-red-400" },
};

const extraNotifications: Notification[] = [
  {
    id: "n-5",
    title: "Report Generated",
    message: "Weekly Sales Report is ready for download.",
    type: "success",
    read: false,
    createdAt: "2026-07-29T08:00:00Z",
    actionUrl: "/reports",
  },
  {
    id: "n-6",
    title: "Storage Limit Warning",
    message: "You've used 85% of your storage quota.",
    type: "warning",
    read: true,
    createdAt: "2026-07-28T16:30:00Z",
    actionUrl: "/billing",
  },
  {
    id: "n-7",
    title: "Dashboard Shared",
    message: "Marcus Johnson shared Sales Performance with you.",
    type: "info",
    read: true,
    createdAt: "2026-07-27T11:00:00Z",
    actionUrl: "/dashboard",
  },
];

function groupByDate(notifications: Notification[]) {
  const groups: Record<string, Notification[]> = {};
  const today = new Date("2026-07-31");
  const yesterday = new Date("2026-07-30");

  notifications.forEach((n) => {
    const date = new Date(n.createdAt);
    let label: string;
    if (date.toDateString() === today.toDateString()) label = "Today";
    else if (date.toDateString() === yesterday.toDateString()) label = "Yesterday";
    else label = date.toLocaleDateString("en-US", { weekday: "long", month: "short", day: "numeric" });
    if (!groups[label]) groups[label] = [];
    groups[label].push(n);
  });
  return groups;
}

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([...mockNotifications, ...extraNotifications]);
  const [filter, setFilter] = useState<"all" | "unread" | Notification["type"]>("all");

  const filtered = useMemo(() => {
    if (filter === "all") return notifications;
    if (filter === "unread") return notifications.filter((n) => !n.read);
    return notifications.filter((n) => n.type === filter);
  }, [notifications, filter]);

  const grouped = useMemo(() => groupByDate(filtered), [filtered]);
  const unreadCount = notifications.filter((n) => !n.read).length;

  const markAsRead = (id: string) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)));
  };

  const markAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  return (
    <PageContainer>
      <PageHeader
        title="Notifications"
        description="Stay updated on datasets, workflows, AI insights, and team activity."
        actions={
          <>
            <Button variant="outline" size="sm" className="gap-1.5" disabled={unreadCount === 0} onClick={markAllRead}>
              <CheckCheck className="h-3.5 w-3.5" /> Mark all read
            </Button>
          </>
        }
      />

      <PageSection>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <MetricCard label="Total" value={notifications.length} icon={Bell} delay={0} />
          <MetricCard label="Unread" value={unreadCount} change={unreadCount > 0 ? 12 : 0} changeType="increase" icon={Filter} delay={0.1} />
          <MetricCard label="This Week" value={notifications.length} icon={CheckCircle2} delay={0.2} />
        </div>
      </PageSection>

      <PageSection>
        <Tabs value={filter} onValueChange={(v) => setFilter(v as typeof filter)}>
          <TabsList className="bg-muted/50">
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="unread">Unread ({unreadCount})</TabsTrigger>
            <TabsTrigger value="success">Success</TabsTrigger>
            <TabsTrigger value="info">Info</TabsTrigger>
            <TabsTrigger value="error">Errors</TabsTrigger>
            <TabsTrigger value="warning">Warnings</TabsTrigger>
          </TabsList>
        </Tabs>
      </PageSection>

      <PageSection>
        <div className="space-y-8">
          {Object.entries(grouped).map(([date, items]) => (
            <div key={date}>
              <h3 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wider">{date}</h3>
              <div className="space-y-2">
                <AnimatePresence>
                  {items.map((notification, i) => {
                    const config = typeConfig[notification.type];
                    const Icon = config.icon;
                    return (
                      <motion.div
                        key={notification.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ delay: i * 0.05 }}
                      >
                        <GlassCard
                          className={`p-4 ${!notification.read ? "border-primary/30 bg-primary/5" : ""}`}
                          hover
                          delay={0}
                        >
                          <div className="flex gap-4">
                            <div className={`mt-0.5 rounded-lg bg-muted/50 p-2 ${config.color}`}>
                              <Icon className="h-4 w-4" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-start justify-between gap-2">
                                <div>
                                  <div className="flex items-center gap-2">
                                    <p className="text-sm font-medium">{notification.title}</p>
                                    {!notification.read && (
                                      <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                                    )}
                                  </div>
                                  <p className="text-sm text-muted-foreground mt-1">{notification.message}</p>
                                  <p className="text-xs text-muted-foreground/60 mt-2">
                                    {formatRelativeTime(notification.createdAt)}
                                  </p>
                                </div>
                                <Badge variant={config.badge}>{notification.type}</Badge>
                              </div>
                              <div className="flex items-center gap-2 mt-3">
                                {!notification.read && (
                                  <Button variant="ghost" size="sm" className="h-7 text-xs" onClick={() => markAsRead(notification.id)}>
                                    Mark read
                                  </Button>
                                )}
                                {notification.actionUrl && (
                                  <Link href={notification.actionUrl}>
                                    <Button variant="outline" size="sm" className="h-7 text-xs gap-1">
                                      View <ExternalLink className="h-3 w-3" />
                                    </Button>
                                  </Link>
                                )}
                              </div>
                            </div>
                          </div>
                        </GlassCard>
                      </motion.div>
                    );
                  })}
                </AnimatePresence>
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <GlassCard className="text-center py-12">
              <Bell className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
              <p className="text-muted-foreground">No notifications match your filter.</p>
            </GlassCard>
          )}
        </div>
      </PageSection>
    </PageContainer>
  );
}
