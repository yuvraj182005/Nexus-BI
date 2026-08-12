"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent } from "@/components/ui/card";
import { HelpCircle, BookOpen, MessageSquare, ExternalLink } from "lucide-react";
import Link from "next/link";
import { ROUTES } from "@/lib/constants";

export default function HelpCenterPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Help Center & Support"
        description="Access technical guides, API documentation, and 24/7 enterprise support."
      />

      <PageSection>
        <div className="grid md:grid-cols-3 gap-4">
          <Link href={ROUTES.docs}>
            <Card className="glass-panel border-white/[0.08] hover:border-primary/40 transition-all p-5">
              <BookOpen className="h-6 w-6 text-indigo-400 mb-2" />
              <h3 className="text-sm font-semibold text-foreground">API Documentation</h3>
              <p className="text-xs text-muted-foreground mt-1">Explore REST and GraphQL APIs</p>
            </Card>
          </Link>

          <Link href={ROUTES.chat}>
            <Card className="glass-panel border-white/[0.08] hover:border-primary/40 transition-all p-5">
              <MessageSquare className="h-6 w-6 text-emerald-400 mb-2" />
              <h3 className="text-sm font-semibold text-foreground">AI Support Agent</h3>
              <p className="text-xs text-muted-foreground mt-1">Instant query debugging with AI</p>
            </Card>
          </Link>

          <Card className="glass-panel border-white/[0.08] p-5">
            <HelpCircle className="h-6 w-6 text-cyan-400 mb-2" />
            <h3 className="text-sm font-semibold text-foreground">Enterprise SLA</h3>
            <p className="text-xs text-muted-foreground mt-1">Dedicated 15-min response guarantee</p>
          </Card>
        </div>
      </PageSection>
    </PageContainer>
  );
}
