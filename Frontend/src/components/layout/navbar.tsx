"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  Search,
  Bell,
  Bot,
  Menu,
  Command,
  LogOut,
  User,
  Settings,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { useUIStore } from "@/stores/ui-store";
import { useAuthStore } from "@/stores/auth-store";
import { getInitials } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

export function Navbar() {
  const router = useRouter();
  const {
    setSidebarMobileOpen,
    setCommandPaletteOpen,
    toggleCopilot,
    unreadCount,
    notifications,
    markNotificationRead,
  } = useUIStore();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    router.push(ROUTES.login);
  };

  return (
    <motion.header
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-0 z-30 flex h-16 w-full items-center justify-between gap-4 border-b border-white/[0.08] bg-background/70 backdrop-blur-xl px-4 md:px-6"
    >
      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          className="lg:hidden"
          onClick={() => setSidebarMobileOpen(true)}
        >
          <Menu className="h-5 w-5" />
        </Button>

        {/* Global Keyboard Search Bar Trigger */}
        <button
          onClick={() => setCommandPaletteOpen(true)}
          className="relative flex items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.03] px-3.5 py-1.5 text-xs text-muted-foreground transition-all duration-300 hover:bg-white/[0.06] hover:border-white/[0.15] hover:text-foreground w-48 sm:w-64 md:w-80 group shadow-sm"
        >
          <Search className="h-3.5 w-3.5 text-muted-foreground group-hover:text-primary transition-colors" />
          <span className="truncate">Search queries, datasets, models...</span>
          <kbd className="ml-auto pointer-events-none hidden h-5 select-none items-center gap-0.5 rounded border border-white/[0.1] bg-muted/60 px-1.5 font-mono text-[10px] font-medium sm:flex">
            <Command className="h-3 w-3" />K
          </kbd>
        </button>
      </div>

      <div className="flex items-center gap-2">
        {/* Copilot Action Trigger */}
        <Button
          variant="outline"
          size="sm"
          onClick={toggleCopilot}
          className="relative gap-2 border-primary/30 bg-primary/10 text-primary hover:bg-primary/20 hover:text-primary transition-all duration-300 shadow-glow"
        >
          <Sparkles className="h-3.5 w-3.5 animate-spin" style={{ animationDuration: "8s" }} />
          <span className="hidden sm:inline text-xs font-semibold">AI Copilot</span>
          <kbd className="hidden md:inline-flex h-4 items-center rounded border border-primary/30 bg-primary/20 px-1 font-mono text-[9px]">
            ⌘J
          </kbd>
        </Button>

        {/* Notifications Popover */}
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="ghost" size="icon" className="relative rounded-full hover:bg-white/[0.06]">
              <Bell className="h-4 w-4" />
              {unreadCount > 0 && (
                <span className="absolute top-1.5 right-1.5 flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                </span>
              )}
            </Button>
          </PopoverTrigger>
          <PopoverContent align="end" className="w-80 glass-strong p-0 border-white/[0.1]">
            <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
              <div className="flex items-center gap-2">
                <Bell className="h-4 w-4 text-primary" />
                <span className="text-sm font-semibold">Notifications</span>
              </div>
              <Badge variant="outline" className="text-[10px] bg-primary/10 text-primary border-primary/30">
                {unreadCount} New
              </Badge>
            </div>
            <div className="max-h-72 overflow-y-auto divide-y divide-white/[0.04]">
              {notifications.length > 0 ? (
                notifications.slice(0, 4).map((n) => (
                  <div
                    key={n.id}
                    onClick={() => markNotificationRead(n.id)}
                    className="p-3 text-xs hover:bg-white/[0.03] transition-colors cursor-pointer"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-medium text-foreground">{n.title}</p>
                      {!n.read && <span className="h-1.5 w-1.5 rounded-full bg-primary shrink-0 mt-1" />}
                    </div>
                    <p className="text-muted-foreground mt-0.5 line-clamp-2">{n.message}</p>
                    <p className="text-[10px] text-muted-foreground/60 mt-1">{n.createdAt}</p>
                  </div>
                ))
              ) : (
                <div className="p-6 text-center text-xs text-muted-foreground">
                  <CheckCircle2 className="h-6 w-6 text-emerald-400 mx-auto mb-2 opacity-80" />
                  All caught up! No unread alerts.
                </div>
              )}
            </div>
            <div className="border-t border-white/[0.08] p-2 text-center">
              <Link href={ROUTES.notifications} className="text-xs text-primary font-medium hover:underline">
                View all notifications →
              </Link>
            </div>
          </PopoverContent>
        </Popover>

        {/* User Profile Menu */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-9 w-9 rounded-full hover:bg-white/[0.06] p-0 ml-1">
              <Avatar className="h-8 w-8 border border-white/[0.12]">
                <AvatarFallback className="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 text-indigo-300 text-xs font-semibold">
                  {getInitials(user?.name || "K Bhramee")}
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56 glass-strong border-white/[0.1]">
            <div className="px-3 py-2">
              <p className="text-xs font-semibold text-foreground">{user?.name || "K Bhramee Sundaram"}</p>
              <p className="text-[11px] text-muted-foreground truncate">{user?.email || "bhramee@nexusbi.ai"}</p>
              <div className="mt-1.5 inline-flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full">
                <ShieldCheck className="h-3 w-3" /> Enterprise Admin
              </div>
            </div>
            <DropdownMenuSeparator className="bg-white/[0.08]" />
            <DropdownMenuItem asChild className="cursor-pointer text-xs focus:bg-white/[0.06]">
              <Link href={ROUTES.profile}>
                <User className="mr-2 h-3.5 w-3.5 text-muted-foreground" /> Profile & Account
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild className="cursor-pointer text-xs focus:bg-white/[0.06]">
              <Link href={ROUTES.settings}>
                <Settings className="mr-2 h-3.5 w-3.5 text-muted-foreground" /> Workspace Settings
              </Link>
            </DropdownMenuItem>
            <DropdownMenuSeparator className="bg-white/[0.08]" />
            <DropdownMenuItem onClick={handleLogout} className="cursor-pointer text-xs text-rose-400 focus:bg-rose-500/10">
              <LogOut className="mr-2 h-3.5 w-3.5 text-rose-400" /> Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </motion.header>
  );
}
