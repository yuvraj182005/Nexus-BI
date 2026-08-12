"use client";

import { PageContainer, PageHeader, PageSection } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BookOpen, Terminal, Code2, Shield } from "lucide-react";

export default function DocumentationPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Developer Documentation & API Guides"
        description="Comprehensive reference for NexusBI AI OpenAPI endpoints, SDKs, and webhook events."
      />

      <PageSection>
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="glass-panel border-white/[0.08]">
            <CardHeader>
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Terminal className="h-4 w-4 text-indigo-400" /> Fast REST API Endpoints
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-xs font-mono text-indigo-300">
              <p>GET /api/v1/health</p>
              <p>POST /api/v1/auth/login</p>
              <p>POST /api/v1/sql/generate</p>
              <p>POST /api/v1/forecasting/generate</p>
              <p>POST /api/v1/copilot</p>
            </CardContent>
          </Card>

          <Card className="glass-panel border-white/[0.08]">
            <CardHeader>
              <CardTitle className="text-sm font-semibold flex items-center gap-2">
                <Shield className="h-4 w-4 text-emerald-400" /> Authentication & Security
              </CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground leading-relaxed">
              All requests require a Bearer token in the Authorization header. Obtain tokens via POST /api/v1/auth/login.
            </CardContent>
          </Card>
        </div>
      </PageSection>
    </PageContainer>
  );
}
