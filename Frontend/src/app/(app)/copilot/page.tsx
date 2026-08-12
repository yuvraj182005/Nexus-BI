"use client";

import { PageContainer, PageHeader } from "@/components/common/page-header";
import { CopilotPanel } from "@/components/layout/copilot-panel";

export default function CopilotPage() {
  return (
    <PageContainer>
      <PageHeader
        title="AI Copilot Studio"
        description="Full-screen AI decision intelligence agent for natural language analytics, forecasting, and data manipulation."
      />
      <div className="relative min-h-[500px]">
        <CopilotPanel />
      </div>
    </PageContainer>
  );
}
