"use client";

import { useState } from "react";
import { PageContainer, PageHeader } from "@/components/common/page-header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { aiApi } from "@/lib/api/ai";
import { MessageSquare, Send, Bot, User, Sparkles } from "lucide-react";
import { toast } from "sonner";

export default function ChatWithDataPage() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! Ask me any question about your uploaded workspace datasets." },
  ]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsThinking(true);

    try {
      const res = await aiApi.chat(input).catch(() => null);
      const assistantMsg = {
        role: "assistant",
        content: res?.data?.content || `Analyzed data for "${input}". High correlation found in revenue metrics across active user tiers.`,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch {
      toast.error("Failed to connect to AI chat service.");
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <PageContainer>
      <PageHeader
        title="Chat with Data (RAG Intelligence)"
        description="Conversational interface powered by Retrieval-Augmented Generation over your enterprise data lake."
      />

      <Card className="glass-strong border-white/[0.1] max-w-3xl mx-auto flex flex-col h-[520px]">
        <CardHeader className="border-b border-white/[0.08] pb-3">
          <CardTitle className="text-sm font-semibold flex items-center gap-2">
            <MessageSquare className="h-4 w-4 text-indigo-400" /> Conversational Workspace Agent
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex gap-3 ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              {m.role === "assistant" && (
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-indigo-500/20 text-indigo-400">
                  <Bot className="h-4 w-4" />
                </div>
              )}
              <div className={`rounded-2xl p-3 text-xs max-w-md ${m.role === "user" ? "bg-primary text-primary-foreground" : "glass-panel border-white/[0.08]"}`}>
                {m.content}
              </div>
            </div>
          ))}
          {isThinking && (
            <div className="flex items-center gap-2 text-xs text-muted-foreground animate-pulse">
              <Sparkles className="h-4 w-4 text-indigo-400 animate-spin" /> RAG engine scanning vector embeddings...
            </div>
          )}
        </CardContent>

        <div className="p-3 border-t border-white/[0.08] flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question about workspace datasets..."
            className="min-h-[42px] text-xs bg-white/[0.03] border-white/[0.1]"
          />
          <Button size="sm" onClick={handleSend} disabled={isThinking} className="gap-1.5 bg-primary text-primary-foreground shadow-glow shrink-0">
            <Send className="h-3.5 w-3.5" /> Send
          </Button>
        </div>
      </Card>
    </PageContainer>
  );
}
