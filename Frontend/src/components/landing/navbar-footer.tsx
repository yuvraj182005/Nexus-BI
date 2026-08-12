"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Hexagon } from "lucide-react";
import { APP_NAME, ROUTES } from "@/lib/constants";

const footerLinks = {
  Product: ["Features", "Pricing", "Integrations", "Changelog", "Roadmap"],
  Platform: ["Analytics", "AI Copilot", "Forecasting", "Workflows", "Governance"],
  Resources: ["Documentation", "API Reference", "Blog", "Community", "Status"],
  Company: ["About", "Careers", "Contact", "Partners", "Press"],
};

export function LandingNavbar() {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/[0.06]"
    >
      <div className="mx-auto max-w-7xl flex items-center justify-between px-6 h-16">
        <Link href="/" className="flex items-center gap-2">
          <Hexagon className="h-6 w-6 text-primary" />
          <span className="font-bold text-sm">{APP_NAME}</span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {["Features", "Architecture", "Security", "Pricing", "FAQ"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              {item}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <Link href={ROUTES.login} className="text-sm text-muted-foreground hover:text-foreground transition-colors hidden sm:block">
            Sign In
          </Link>
          <Link
            href={ROUTES.register}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </div>
    </motion.nav>
  );
}

export function LandingFooter() {
  return (
    <footer className="border-t border-border py-16">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <Hexagon className="h-6 w-6 text-primary" />
              <span className="font-bold text-sm">{APP_NAME}</span>
            </Link>
            <p className="text-sm text-muted-foreground leading-relaxed">
              One Intelligent Platform for Data, Analytics, AI & Business Decisions.
            </p>
          </div>
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-semibold text-sm mb-3">{category}</h4>
              <ul className="space-y-2">
                {links.map((link) => (
                  <li key={link}>
                    <span className="text-sm text-muted-foreground hover:text-foreground transition-colors cursor-pointer">
                      {link}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 pt-8 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground">
            &copy; 2026 {APP_NAME}. All rights reserved.
          </p>
          <div className="flex gap-6">
            {["Privacy", "Terms", "Security", "Cookies"].map((item) => (
              <span key={item} className="text-xs text-muted-foreground hover:text-foreground cursor-pointer transition-colors">
                {item}
              </span>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

export function CTASection() {
  return (
    <section className="py-24 relative">
      <div className="mx-auto max-w-4xl px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="glass-strong rounded-2xl p-12 shadow-glow-lg"
        >
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight">
            Ready to transform your{" "}
            <span className="gradient-text">data strategy</span>?
          </h2>
          <p className="mt-4 text-muted-foreground text-lg max-w-xl mx-auto">
            Join thousands of enterprises using NexusBI AI to make smarter, faster decisions.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              href={ROUTES.register}
              className="rounded-lg bg-primary px-8 py-3 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors shadow-glow"
            >
              Start Free Trial
            </Link>
            <Link
              href={ROUTES.login}
              className="rounded-lg border border-border px-8 py-3 text-sm font-medium hover:bg-secondary/50 transition-colors"
            >
              Sign In to Demo
            </Link>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
