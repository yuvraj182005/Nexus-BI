import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Toaster } from "sonner";
import { QueryProvider } from "@/providers/query-provider";
import { KeyboardShortcuts } from "@/providers/keyboard-shortcuts";
import { TooltipProvider } from "@/components/ui/tooltip";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-geist-sans",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  title: "NexusBI AI — Enterprise Decision Intelligence Platform",
  description:
    "One Intelligent Platform for Data, Analytics, AI & Business Decisions. Connect data sources, build dashboards, forecast trends, and govern enterprise data.",
  keywords: [
    "business intelligence",
    "analytics",
    "AI",
    "data platform",
    "forecasting",
    "dashboards",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrains.variable} font-sans antialiased`}>
        <QueryProvider>
          <TooltipProvider>
            {children}
            <KeyboardShortcuts />
            <Toaster
              theme="dark"
              position="bottom-right"
              toastOptions={{
                style: {
                  background: "hsl(222 47% 8%)",
                  border: "1px solid hsl(217 33% 16%)",
                  color: "hsl(210 40% 98%)",
                },
              }}
            />
          </TooltipProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
