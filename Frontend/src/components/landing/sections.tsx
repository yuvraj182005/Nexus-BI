"use client";

import { motion } from "framer-motion";
import { Shield, Lock, Eye, FileCheck, Server, Key } from "lucide-react";

const securityFeatures = [
  { icon: Lock, title: "End-to-End Encryption", description: "AES-256 encryption at rest and TLS 1.3 in transit" },
  { icon: Key, title: "SSO & MFA", description: "SAML 2.0, OIDC, and multi-factor authentication" },
  { icon: Eye, title: "Row-Level Security", description: "Granular data access controls at the row and column level" },
  { icon: FileCheck, title: "Compliance Ready", description: "SOC 2 Type II, GDPR, HIPAA, and ISO 27001 certified" },
  { icon: Server, title: "Private Deployment", description: "VPC, on-premise, and air-gapped deployment options" },
  { icon: Shield, title: "Audit & Lineage", description: "Complete audit trails and data lineage tracking" },
];

export function SecuritySection() {
  return (
    <section id="security" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Enterprise-Grade <span className="gradient-text">Security</span>
          </h2>
          <p className="mt-4 text-muted-foreground max-w-2xl mx-auto text-lg">
            Built for the most demanding security and compliance requirements.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {securityFeatures.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
              className="rounded-xl border border-border bg-card p-6 hover:border-emerald-500/30 transition-colors"
            >
              <div className="rounded-lg bg-emerald-500/10 w-fit p-2.5 mb-4">
                <feature.icon className="h-5 w-5 text-emerald-400" />
              </div>
              <h3 className="font-semibold mb-2">{feature.title}</h3>
              <p className="text-sm text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

const testimonials = [
  {
    quote: "NexusBI AI transformed how our 500-person analytics team operates. We went from weeks to hours for insight delivery.",
    author: "Sarah Chen",
    role: "VP of Data, Fortune 500 Retail",
    avatar: "SC",
  },
  {
    quote: "The AI copilot alone saved us 40% of analyst time. Natural language to SQL is genuinely production-ready.",
    author: "Marcus Johnson",
    role: "Head of Analytics, Global Finance Corp",
    avatar: "MJ",
  },
  {
    quote: "Finally, a platform that unifies our data stack. Governance, analytics, and AI in one place — not five different tools.",
    author: "Elena Rodriguez",
    role: "CDO, Healthcare Enterprise",
    avatar: "ER",
  },
];

export function TestimonialsSection() {
  return (
    <section id="testimonials" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Trusted by <span className="gradient-text">Industry Leaders</span>
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.author}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass rounded-xl p-6"
            >
              <p className="text-sm leading-relaxed mb-6">&ldquo;{t.quote}&rdquo;</p>
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-sm font-medium text-primary">
                  {t.avatar}
                </div>
                <div>
                  <p className="text-sm font-medium">{t.author}</p>
                  <p className="text-xs text-muted-foreground">{t.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

const plans = [
  {
    name: "Starter",
    price: 49,
    description: "For small teams getting started with data analytics",
    features: ["5 users", "10 datasets", "Basic dashboards", "AI Copilot (100 queries/mo)", "Email support"],
    highlighted: false,
  },
  {
    name: "Professional",
    price: 149,
    description: "For growing teams that need advanced analytics",
    features: ["25 users", "Unlimited datasets", "Advanced dashboards", "AI Copilot (unlimited)", "Forecasting", "Workflows", "Priority support"],
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: null,
    description: "For organizations with advanced security and scale needs",
    features: ["Unlimited users", "Private deployment", "SSO & SAML", "Custom governance", "Dedicated CSM", "SLA guarantee", "On-premise option"],
    highlighted: false,
  },
];

export function PricingSection() {
  return (
    <section id="pricing" className="py-24 relative">
      <div className="mx-auto max-w-7xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Simple, Transparent <span className="gradient-text">Pricing</span>
          </h2>
          <p className="mt-4 text-muted-foreground max-w-2xl mx-auto text-lg">
            Start free, scale as you grow. No hidden fees.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan, i) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className={`rounded-xl border p-6 ${
                plan.highlighted
                  ? "border-primary/50 bg-primary/5 shadow-glow"
                  : "border-border bg-card"
              }`}
            >
              {plan.highlighted && (
                <span className="text-xs font-medium text-primary bg-primary/10 rounded-full px-3 py-1">
                  Most Popular
                </span>
              )}
              <h3 className="text-xl font-bold mt-4">{plan.name}</h3>
              <p className="text-sm text-muted-foreground mt-1">{plan.description}</p>
              <div className="mt-4 mb-6">
                {plan.price ? (
                  <div>
                    <span className="text-4xl font-bold">${plan.price}</span>
                    <span className="text-muted-foreground">/user/mo</span>
                  </div>
                ) : (
                  <span className="text-4xl font-bold">Custom</span>
                )}
              </div>
              <ul className="space-y-2.5 mb-6">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm">
                    <div className="h-1.5 w-1.5 rounded-full bg-primary shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <button
                className={`w-full rounded-lg py-2.5 text-sm font-medium transition-colors ${
                  plan.highlighted
                    ? "bg-primary text-primary-foreground hover:bg-primary/90"
                    : "border border-border hover:bg-secondary/50"
                }`}
              >
                {plan.price ? "Start Free Trial" : "Contact Sales"}
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

const faqs = [
  { q: "How does NexusBI AI differ from Power BI or Tableau?", a: "NexusBI AI is a unified platform combining BI, AI, data engineering, and governance — not just visualization. Our AI copilot, semantic layer, and workflow automation are built-in, not bolted on." },
  { q: "Can I connect my existing data warehouse?", a: "Yes. We support 200+ connectors including Snowflake, Databricks, BigQuery, Redshift, PostgreSQL, and more. Data stays in your warehouse — we query it in place." },
  { q: "Is my data secure?", a: "Absolutely. We are SOC 2 Type II certified with end-to-end encryption, row-level security, and support for VPC and on-premise deployment." },
  { q: "How does the AI Copilot work?", a: "Our copilot understands your semantic model and can generate SQL, create visualizations, explain trends, and automate reports — all through natural language." },
  { q: "Can I try before I buy?", a: "Yes! Start with a 14-day free trial of the Professional plan. No credit card required." },
];

export function FAQSection() {
  return (
    <section id="faq" className="py-24 relative">
      <div className="mx-auto max-w-3xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
            Frequently Asked <span className="gradient-text">Questions</span>
          </h2>
        </motion.div>

        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <motion.details
              key={faq.q}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="group rounded-xl border border-border bg-card p-5 cursor-pointer"
            >
              <summary className="font-medium text-sm list-none flex items-center justify-between">
                {faq.q}
                <span className="text-muted-foreground group-open:rotate-45 transition-transform text-lg">+</span>
              </summary>
              <p className="mt-3 text-sm text-muted-foreground leading-relaxed">{faq.a}</p>
            </motion.details>
          ))}
        </div>
      </div>
    </section>
  );
}
