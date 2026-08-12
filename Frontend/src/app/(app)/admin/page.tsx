"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Settings2, ShieldCheck, Users, Building2 } from "lucide-react";

export default function AdminPortalPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Enterprise Admin Portal"
        description="Manage multi-tenant organization settings, SSO authentication, and platform licenses."
      />

      <PageSection>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card className="glass-panel border-white/[0.08] p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                <Building2 className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs font-semibold text-foreground">Organization Tenant</p>
                <p className="text-[10px] text-muted-foreground mt-0.5">NexusBI Enterprise Corp</p>
              </div>
            </div>
          </Card>

          <Card className="glass-panel border-white/[0.08] p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs font-semibold text-foreground">SAML 2.0 / Okta SSO</p>
                <p className="text-[10px] text-emerald-400 mt-0.5">Active & Verified</p>
              </div>
            </div>
          </Card>

          <Card className="glass-panel border-white/[0.08] p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                <Users className="h-5 w-5" />
              </div>
              <div>
                <p className="text-xs font-semibold text-foreground">Provisioned Users</p>
                <p className="text-[10px] text-muted-foreground mt-0.5">12 / 50 Enterprise Seats</p>
              </div>
            </div>
          </Card>
        </div>
      </PageSection>
    </PageContainer>
  );
}
