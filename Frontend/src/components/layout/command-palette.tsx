"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Command as CommandPrimitive } from "cmdk";
import {
  Search,
  LayoutDashboard,
  Database,
  Settings,
  Terminal,
  Upload,
  Store,
  Bell,
  User,
  Plus,
  Sparkles,
} from "lucide-react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { useUIStore } from "@/stores/ui-store";
import { ROUTES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { platformApi } from "@/lib/api/platform";

interface CommandItem {
  label: string;
  href?: string;
  action?: string;
  icon: React.ComponentType<{ className?: string }>;
  shortcut?: string;
}

interface CommandGroup {
  group: string;
  items: CommandItem[];
}

const commandGroups: CommandGroup[] = [
  {
    group: "Navigation",
    items: [
      { label: "Executive Dashboard", href: ROUTES.dashboard, icon: LayoutDashboard, shortcut: "G D" },
      { label: "AI Data Studio", href: ROUTES.workspace, icon: Terminal, shortcut: "G W" },
      { label: "Datasets Catalog", href: ROUTES.datasets, icon: Database, shortcut: "G DS" },
      { label: "Upload New Dataset", href: ROUTES.datasetUpload, icon: Upload, shortcut: "G U" },
      { label: "Connector Marketplace", href: ROUTES.marketplace, icon: Store, shortcut: "G M" },
      { label: "Notifications & Alerts", href: ROUTES.notifications, icon: Bell, shortcut: "G N" },
      { label: "Workspace Settings", href: ROUTES.settings, icon: Settings, shortcut: "G S" },
    ],
  },
  {
    group: "Quick Actions",
    items: [
      { label: "Ask AI Copilot", action: "copilot", icon: Sparkles, shortcut: "⌘J" },
      { label: "New Custom Dashboard", href: ROUTES.dashboardBuilder, icon: Plus },
      { label: "Run SQL Query", href: ROUTES.sqlStudio, icon: Terminal },
      { label: "View Profile & Permissions", href: ROUTES.profile, icon: User },
    ],
  },
  {
    group: "Enterprise Data Sources",
    items: [
      { label: "PostgreSQL Production DB", href: ROUTES.datasets, icon: Database },
      { label: "Snowflake Analytics Warehouse", href: ROUTES.datasets, icon: Database },
      { label: "BigQuery Customer Stream", href: ROUTES.datasets, icon: Database },
      { label: "Amazon S3 Data Lake", href: ROUTES.datasets, icon: Database },
    ],
  },
];

export function CommandPalette() {
  const router = useRouter();
  const { commandPaletteOpen, setCommandPaletteOpen, toggleCopilot } = useUIStore();
  const [search, setSearch] = useState("");

  // Global listener for Cmd+K / Ctrl+K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setCommandPaletteOpen(!commandPaletteOpen);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [commandPaletteOpen, setCommandPaletteOpen]);

  useEffect(() => {
    if (!commandPaletteOpen) setSearch("");
    if (search.trim().length > 2) {
      platformApi.search(search).catch(() => null);
    }
  }, [commandPaletteOpen, search]);

  const handleSelect = (item: CommandItem) => {
    setCommandPaletteOpen(false);
    if (item.action === "copilot") {
      toggleCopilot();
    } else if (item.href) {
      router.push(item.href);
    }
  };

  return (
    <Dialog open={commandPaletteOpen} onOpenChange={setCommandPaletteOpen}>
      <DialogContent className="overflow-hidden p-0 glass-strong border-white/[0.12] max-w-xl shadow-2xl rounded-2xl">
        <CommandPrimitive className="[&_[cmdk-group-heading]]:px-3 [&_[cmdk-group-heading]]:py-2 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:font-semibold [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-wider [&_[cmdk-group-heading]]:text-muted-foreground">
          <div className="flex items-center border-b border-white/[0.08] px-4">
            <Search className="mr-3 h-4 w-4 shrink-0 opacity-60 text-primary" />
            <CommandPrimitive.Input
              value={search}
              onValueChange={setSearch}
              placeholder="Search anything across workspace... (e.g. Revenue, Datasets, Settings)"
              className="flex h-13 w-full bg-transparent py-3.5 text-xs outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed"
            />
            <kbd className="hidden sm:inline-flex h-5 items-center rounded border border-white/[0.1] bg-muted/60 px-1.5 font-mono text-[10px] text-muted-foreground">
              ESC
            </kbd>
          </div>
          <CommandPrimitive.List className="max-h-[340px] overflow-y-auto p-2">
            <CommandPrimitive.Empty className="py-8 text-center text-xs text-muted-foreground">
              No matching pages, queries, or datasets found.
            </CommandPrimitive.Empty>
            {commandGroups.map((group) => (
              <CommandPrimitive.Group key={group.group} heading={group.group}>
                {group.items.map((item) => (
                  <CommandPrimitive.Item
                    key={item.label}
                    value={item.label}
                    onSelect={() => handleSelect(item)}
                    className={cn(
                      "relative flex cursor-pointer select-none items-center rounded-xl px-3 py-2.5 text-xs outline-none transition-all duration-150",
                      "aria-selected:bg-primary/15 aria-selected:text-primary font-medium"
                    )}
                  >
                    <item.icon className="mr-3 h-4 w-4 shrink-0 text-muted-foreground group-aria-selected:text-primary" />
                    <span>{item.label}</span>
                    {item.shortcut && (
                      <kbd className="ml-auto pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-white/[0.1] bg-white/[0.05] px-1.5 font-mono text-[10px] text-muted-foreground">
                        {item.shortcut}
                      </kbd>
                    )}
                  </CommandPrimitive.Item>
                ))}
              </CommandPrimitive.Group>
            ))}
          </CommandPrimitive.List>
          <div className="flex items-center justify-between border-t border-white/[0.08] px-4 py-2 text-[10px] text-muted-foreground/70 bg-white/[0.02]">
            <span>Navigate with ↑ ↓ and press Enter</span>
            <span>NexusBI AI Command Center</span>
          </div>
        </CommandPrimitive>
      </DialogContent>
    </Dialog>
  );
}
