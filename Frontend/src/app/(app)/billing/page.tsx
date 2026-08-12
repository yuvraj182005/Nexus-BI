"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CreditCard, Zap, CheckCircle2 } from "lucide-react";

export default function BillingPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Usage & Billing Center"
        description="Monitor compute credits, API call quotas, vector storage utilization, and subscription invoices."
      />

      <PageSection>
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <CreditCard className="h-4 w-4 text-indigo-400" /> Active Subscription Plan
                </span>
                <Badge className="bg-emerald-500/10 text-emerald-400 border-emerald-500/20 text-[10px]">
                  Enterprise Annual
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 pt-2 text-xs">
              <p className="text-muted-foreground">Unlimited Datasets · Priority AI Gateway · Dedicated VPC</p>
              <p className="text-sm font-bold text-foreground">$12,000 / year (Renews Sep 2026)</p>
            </CardContent>
          </Card>

          <Card className="glass-panel border-white/[0.08]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Zap className="h-4 w-4 text-amber-400" /> Monthly API & Compute Usage
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 pt-2 text-xs">
              <p className="text-muted-foreground">API Requests: 142,800 / 1,000,000</p>
              <p className="text-muted-foreground">Vector Embeddings: 48.2 GB / 500 GB</p>
            </CardContent>
          </Card>
        </div>
      </PageSection>
    </PageContainer>
  );
}
