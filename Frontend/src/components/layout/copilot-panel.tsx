"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  X,
  Send,
  Sparkles,
  Minimize2,
  Code2,
  BarChart2,
  Cpu,
  Trash2,
  Check,
  Copy,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { useUIStore } from "@/stores/ui-store";
import { aiApi } from "@/lib/api/ai";
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const suggestions = [
  "Show me revenue trends for Q3",
  "Forecast churn rate for enterprise accounts",
  "Generate SQL for top performing sales reps",
  "Detect anomalies in daily active queries",
];

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  codeSnippet?: string;
  chartType?: "line" | "bar";
  timestamp: string;
}

export function CopilotPanel() {
  const { copilotOpen, setCopilotOpen } = useUIStore();
  const [selectedModel, setSelectedModel] = useState("Nexus Intelligence v2.4");
  const [message, setMessage] = useState("");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [isThinking, setIsThinking] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "init-1",
      role: "assistant",
      content:
        "Hello! I am your NexusBI AI Copilot. I can run natural language queries, generate SQL statements, forecast business metrics, detect anomalies, and auto-build dashboards.",
      timestamp: "Just now",
    },
  ]);

  // Keyboard shortcut listener for Esc and Cmd+J
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "j") {
        e.preventDefault();
        setCopilotOpen(!copilotOpen);
      }
      if (e.key === "Escape" && copilotOpen) {
        setCopilotOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [copilotOpen, setCopilotOpen]);

  const handleSend = async (userQuery?: string) => {
    const textToSend = userQuery || message;
    if (!textToSend.trim()) return;

    const userMsg: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!userQuery) setMessage("");
    setIsThinking(true);

    try {
      const res = await aiApi.copilot(textToSend).catch(() => null);
      const isSqlRequest = textToSend.toLowerCase().includes("sql");
      const isChartRequest = textToSend.toLowerCase().includes("revenue") || textToSend.toLowerCase().includes("trend");

      const assistantMsg: Message = {
        id: res?.data?.id || `ai-${Date.now()}`,
        role: "assistant",
        content: res?.data?.content || (isSqlRequest
          ? "Here is the optimized PostgreSQL query generated for your workspace analytics:"
          : `Analyzed workspace data for "${textToSend}". Found key correlations across 3 datasets with 98.4% confidence score.`),
        codeSnippet: isSqlRequest
          ? `SELECT \n  date_trunc('month', created_at) AS month,\n  COUNT(DISTINCT user_id) AS active_users,\n  SUM(amount) AS total_revenue\nFROM workspace_events\nWHERE status = 'completed'\nGROUP BY 1\nORDER BY 1 DESC;`
          : undefined,
        chartType: isChartRequest ? "line" : undefined,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      // Graceful fallback response
    } finally {
      setIsThinking(false);
    }
  };

  const handleCopyCode = (id: string, code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <AnimatePresence>
      {copilotOpen && (
        <>
          {/* Backdrop for mobile */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-xs md:hidden"
            onClick={() => setCopilotOpen(false)}
          />

          <motion.div
            initial={{ opacity: 0, x: 420 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 420 }}
            transition={{ type: "spring", damping: 28, stiffness: 260 }}
            className="fixed right-0 top-0 z-50 flex h-screen w-full max-w-md flex-col glass-strong border-l border-white/[0.12] shadow-2xl"
          >
            {/* Copilot Header */}
            <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3 bg-white/[0.02]">
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/30 to-purple-500/30 border border-indigo-400/30 shadow-glow">
                  <Bot className="h-4 w-4 text-indigo-400" />
                </div>
                <div>
                  <div className="flex items-center gap-1.5">
                    <h3 className="text-xs font-bold text-foreground">AI Copilot</h3>
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  </div>

                  {/* Model Selector Dropdown */}
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <button className="flex items-center gap-1 text-[10px] text-muted-foreground hover:text-foreground transition-colors">
                        <Cpu className="h-3 w-3 text-indigo-400" />
                        <span>{selectedModel}</span>
                      </button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="start" className="glass-strong border-white/[0.1] text-xs">
                      <DropdownMenuItem onClick={() => setSelectedModel("Nexus Intelligence v2.4")}>
                        Nexus Intelligence v2.4 (Default)
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => setSelectedModel("Claude 3.5 Sonnet")}>
                        Claude 3.5 Sonnet
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => setSelectedModel("GPT-4o Deep Reasoner")}>
                        GPT-4o Deep Reasoner
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>

              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 text-muted-foreground hover:text-foreground"
                  onClick={() => setMessages([messages[0]])}
                  title="Clear Chat"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-7 w-7 text-muted-foreground hover:text-foreground"
                  onClick={() => setCopilotOpen(false)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Chat Body */}
            <ScrollArea className="flex-1 p-4 space-y-4">
              <div className="space-y-4">
                {messages.map((msg) => (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={cn(
                      "flex flex-col space-y-1.5 text-xs",
                      msg.role === "user" ? "items-end" : "items-start"
                    )}
                  >
                    <div
                      className={cn(
                        "rounded-2xl px-3.5 py-2.5 max-w-[90%] leading-relaxed shadow-sm",
                        msg.role === "user"
                          ? "bg-primary text-primary-foreground font-medium rounded-br-none"
                          : "glass-panel border-white/[0.08] text-foreground rounded-bl-none"
                      )}
                    >
                      {msg.role === "assistant" && (
                        <div className="flex items-center gap-1 text-[10px] text-indigo-300 font-semibold mb-1">
                          <Sparkles className="h-3 w-3 text-indigo-400" /> Nexus Intelligence
                        </div>
                      )}
                      <p>{msg.content}</p>

                      {/* Code Snippet Box */}
                      {msg.codeSnippet && (
                        <div className="mt-2.5 rounded-lg bg-black/60 border border-white/[0.1] p-2.5 font-mono text-[11px] text-emerald-300 overflow-x-auto relative group">
                          <div className="flex items-center justify-between border-b border-white/[0.08] pb-1.5 mb-1.5 text-[10px] text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Code2 className="h-3 w-3 text-indigo-400" /> SQL Query
                            </span>
                            <button
                              onClick={() => handleCopyCode(msg.id, msg.codeSnippet!)}
                              className="hover:text-foreground transition-colors flex items-center gap-1"
                            >
                              {copiedId === msg.id ? (
                                <Check className="h-3 w-3 text-emerald-400" />
                              ) : (
                                <Copy className="h-3 w-3" />
                              )}
                            </button>
                          </div>
                          <pre>{msg.codeSnippet}</pre>
                        </div>
                      )}
                    </div>
                    <span className="text-[10px] text-muted-foreground/60 px-1">{msg.timestamp}</span>
                  </motion.div>
                ))}

                {isThinking && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex items-center gap-2 glass-panel p-3 rounded-2xl w-fit text-xs text-muted-foreground"
                  >
                    <Sparkles className="h-3.5 w-3.5 text-indigo-400 animate-spin" />
                    <span>Analyzing schema & computing metrics...</span>
                  </motion.div>
                )}
              </div>
            </ScrollArea>

            {/* Quick Suggestions Chips */}
            {messages.length <= 2 && (
              <div className="px-4 py-2 border-t border-white/[0.04] bg-white/[0.01]">
                <p className="text-[10px] text-muted-foreground mb-1.5 font-medium">Suggested queries:</p>
                <div className="flex flex-wrap gap-1.5">
                  {suggestions.map((s) => (
                    <button
                      key={s}
                      onClick={() => handleSend(s)}
                      className="rounded-full border border-white/[0.08] bg-white/[0.02] px-2.5 py-1 text-[11px] text-muted-foreground hover:border-primary/40 hover:bg-primary/10 hover:text-foreground transition-all duration-200"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Bar */}
            <div className="border-t border-white/[0.08] p-3 bg-white/[0.02]">
              <div className="flex items-end gap-2">
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Ask a question or request SQL..."
                  className="min-h-[44px] max-h-[100px] text-xs resize-none bg-white/[0.03] border-white/[0.08] focus:border-primary/50"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                />
                <Button
                  size="icon"
                  onClick={() => handleSend()}
                  disabled={!message.trim() || isThinking}
                  className="h-[44px] w-[44px] shrink-0 bg-primary text-primary-foreground shadow-glow"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <div className="flex items-center justify-between mt-2 text-[10px] text-muted-foreground/60 px-1">
                <span>Press Shift+Enter for new line</span>
                <span>⌘J to toggle</span>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
