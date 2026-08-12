"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion } from "framer-motion";
import { Hexagon, Mail, Lock, User, ArrowRight, Loader2, Building, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { AnimatedBackground } from "@/components/common/animated-background";
import { MouseSpotlight } from "@/components/common/mouse-spotlight";
import { useAuthStore } from "@/stores/auth-store";
import { APP_NAME, ROUTES } from "@/lib/constants";
import { toast } from "sonner";

const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  organization: z.string().optional(),
});

type RegisterForm = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const { setAuth, setLoading, isLoading } = useAuthStore();

  const { register, handleSubmit, formState: { errors } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterForm) => {
    setLoading(true);
    try {
      await new Promise((r) => setTimeout(r, 800));
      setAuth(
        {
          id: "user-new",
          email: data.email,
          name: data.name,
          role: "admin",
          organization: data.organization || "Enterprise Org",
          createdAt: new Date().toISOString(),
        },
        "demo-access-token",
        "demo-refresh-token"
      );
      toast.success("Account created successfully!");
      router.push(ROUTES.dashboard);
    } catch {
      toast.error("Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-6 bg-background mesh-bg noise-texture">
      <MouseSpotlight />
      <AnimatedBackground variant="landing" />

      <motion.div
        initial={{ opacity: 0, y: 25 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2.5 mb-6 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/30 to-purple-500/30 border border-indigo-400/30 shadow-glow group-hover:scale-105 transition-transform">
              <Hexagon className="h-6 w-6 text-indigo-400" />
            </div>
            <span className="font-bold text-xl tracking-tight text-foreground">{APP_NAME}</span>
          </Link>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Start 14-Day Free Trial</h1>
          <p className="text-xs text-muted-foreground mt-1">No credit card required · Unlimited AI queries</p>
        </div>

        <div className="glass-strong rounded-2xl border-white/[0.12] p-8 shadow-2xl space-y-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="name" className="text-xs">Full Name</Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="name" placeholder="K Bhramee Sundaram" className="pl-10 text-xs bg-white/[0.03] border-white/[0.1]" {...register("name")} />
              </div>
              {errors.name && <p className="text-[11px] text-rose-400">{errors.name.message}</p>}
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-xs">Work Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="email" type="email" placeholder="name@company.com" className="pl-10 text-xs bg-white/[0.03] border-white/[0.1]" {...register("email")} />
              </div>
              {errors.email && <p className="text-[11px] text-rose-400">{errors.email.message}</p>}
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="password" className="text-xs">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="password" type="password" placeholder="At least 8 characters" className="pl-10 text-xs bg-white/[0.03] border-white/[0.1]" {...register("password")} />
              </div>
              {errors.password && <p className="text-[11px] text-rose-400">{errors.password.message}</p>}
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="organization" className="text-xs">Organization Name (optional)</Label>
              <div className="relative">
                <Building className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="organization" placeholder="Acme Corp" className="pl-10 text-xs bg-white/[0.03] border-white/[0.1]" {...register("organization")} />
              </div>
            </div>

            <Button type="submit" className="w-full gap-2 bg-primary text-primary-foreground shadow-glow py-5 text-xs font-semibold" disabled={isLoading}>
              {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <>Create Enterprise Account <ArrowRight className="h-4 w-4" /></>}
            </Button>
          </form>

          <div className="relative border-t border-white/[0.08] pt-4 text-center">
            <p className="text-xs text-muted-foreground">
              Already have an account?{" "}
              <Link href={ROUTES.login} className="text-indigo-400 font-semibold hover:underline">
                Sign in
              </Link>
            </p>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-center gap-2 text-[10px] text-muted-foreground">
          <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" /> SOC2 Type II Certified · Instant Setup
        </div>
      </motion.div>
    </div>
  );
}
