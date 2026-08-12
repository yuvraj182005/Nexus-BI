"use client";

import { useQuery } from "@tanstack/react-query";
import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { authApi } from "@/lib/api/auth";
import { getInitials } from "@/lib/utils";
import { User, Mail, Shield, Key } from "lucide-react";

export default function ProfilePage() {
  const { data: currentUser } = useQuery({
    queryKey: ["profile-user"],
    queryFn: () => authApi.me().catch(() => null),
  });

  const user = currentUser?.data || {
    name: "K Bhramee Sundaram",
    email: "bhramee@nexusbi.ai",
    role: "admin",
    organization: "NexusBI Enterprise",
  };

  return (
    <PageContainer>
      <PageHeader
        title="User Profile & Security Credentials"
        description="View personal account profile, role permissions, and active OAuth integrations."
      />

      <PageSection>
        <Card className="glass-panel border-white/[0.08] max-w-xl p-6">
          <div className="flex items-center gap-4">
            <Avatar className="h-16 w-16 border-2 border-primary/50">
              <AvatarFallback className="text-lg bg-primary/20 text-primary font-bold">
                {getInitials(user.name)}
              </AvatarFallback>
            </Avatar>
            <div>
              <h3 className="text-base font-bold text-foreground">{user.name}</h3>
              <p className="text-xs text-muted-foreground">{user.email}</p>
              <p className="text-[11px] text-indigo-400 font-semibold mt-1 capitalize">{user.role} · {user.organization}</p>
            </div>
          </div>
        </Card>
      </PageSection>
    </PageContainer>
  );
}
