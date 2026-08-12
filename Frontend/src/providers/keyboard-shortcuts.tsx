"use client";

import { useEffect } from "react";
import { useUIStore } from "@/stores/ui-store";

export function KeyboardShortcuts() {
  const { setCommandPaletteOpen, toggleCopilot } = useUIStore();

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === "j") {
        e.preventDefault();
        toggleCopilot();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [setCommandPaletteOpen, toggleCopilot]);

  return null;
}
