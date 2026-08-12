"use client";

import { AppShell } from "@/components/layout/app-shell";
import { useUIStore } from "@/stores/ui-store";
import { useEffect } from "react";
import { mockNotifications } from "@/lib/mock-data";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { setNotifications } = useUIStore();

  useEffect(() => {
    setNotifications(mockNotifications);
  }, [setNotifications]);

  return <AppShell>{children}</AppShell>;
}
