"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, Lock, FileCheck, CheckCircle2 } from "lucide-react";

export default function GovernancePage() {
  const policies = [
    { name: "PII Masking & Anonymization", status: "Enforced", scope: "Global Workspace", coverage: "100%" },
    { name: "Row-Level Security (RLS)", status: "Enforced", scope: "PostgreSQL & Snowflake", coverage: "100%" },
    { name: "Role-Based Access Control (RBAC)", status: "Active", scope: "API Gateway", coverage: "100%" },
  ];

  return (
    <PageContainer>
      <PageHeader
        title="Enterprise Data Governance & Compliance"
        description="Enforce security policies, automated PII masking, row-level security (RLS), and data lineage tracking."
      />

      <PageSection>
        <div className="grid md:grid-cols-3 gap-4">
          {policies.map((p, idx) => (
            <Card key={idx} className="glass-panel border-white/[0.08] p-4 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                  <Shield className="h-4 w-4" />
                </div>
                <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                  {p.status}
                </Badge>
              </div>
              <p className="text-xs font-semibold text-foreground pt-2">{p.name}</p>
              <p className="text-[10px] text-muted-foreground">{p.scope} · {p.coverage} Coverage</p>
            </Card>
          ))}
        </div>
      </PageSection>
    </PageContainer>
  );
}
