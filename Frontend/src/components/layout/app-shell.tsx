"use client";

import { Sidebar } from "./sidebar";
import { Navbar } from "./navbar";
import { CommandPalette } from "./command-palette";
import { CopilotPanel } from "./copilot-panel";
import { AnimatedBackground } from "@/components/common/animated-background";
import { MouseSpotlight } from "@/components/common/mouse-spotlight";
import { useUIStore } from "@/stores/ui-store";
import { cn } from "@/lib/utils";

export function AppShell({ children }: { children: React.ReactNode }) {
  const { sidebarCollapsed } = useUIStore();

  return (
    <div className="relative min-h-screen bg-background text-foreground mesh-bg noise-texture">
      <MouseSpotlight />
      <AnimatedBackground variant="app" />
      <Sidebar />
      <div
        className={cn(
          "transition-all duration-300 ease-in-out min-h-screen flex flex-col",
          sidebarCollapsed ? "lg:ml-[64px]" : "lg:ml-[260px]"
        )}
      >
        <Navbar />
        <main className="relative flex-1 p-4 md:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
      <CommandPalette />
      <CopilotPanel />
    </div>
  );
}
