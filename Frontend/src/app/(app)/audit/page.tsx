"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { ActivityFeed } from "@/components/common/activity-feed";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { platformApi } from "@/lib/api/platform";
import { mockActivities } from "@/lib/mock-data";
import { ClipboardList, Clock } from "lucide-react";

export default function AuditCenterPage() {
  const { data: liveAudit } = useQuery({
    queryKey: ["audit-center"],
    queryFn: () => platformApi.audit.list().catch(() => null),
  });

  const activities = liveAudit?.data?.map((a) => ({
    id: a.id,
    type: a.action,
    title: a.action,
    description: a.details || `${a.user} performed ${a.action} on ${a.resource}`,
    user: a.user,
    timestamp: a.timestamp,
  })) || mockActivities;

  return (
    <PageContainer>
      <PageHeader
        title="Audit Log & Security Intelligence"
        description="Immutable compliance audit trail tracking all user authentication, query execution, and API key usages."
      />

      <PageSection>
        <Card className="glass-panel border-white/[0.08]">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base font-semibold flex items-center gap-2">
              <ClipboardList className="h-4 w-4 text-indigo-400" /> Compliance Activity Stream
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ActivityFeed items={activities} />
          </CardContent>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
