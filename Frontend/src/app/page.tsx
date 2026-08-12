import { LandingNavbar, LandingFooter, CTASection } from "@/components/landing/navbar-footer";
import { LandingHero } from "@/components/landing/hero";
import { FeaturesSection, ArchitectureSection } from "@/components/landing/features";
import {
  SecuritySection,
  TestimonialsSection,
  PricingSection,
  FAQSection,
} from "@/components/landing/sections";

export default function HomePage() {
  return (
    <>
      <LandingNavbar />
      <main>
        <LandingHero />
        <FeaturesSection />
        <ArchitectureSection />
        <SecuritySection />
        <TestimonialsSection />
        <PricingSection />
        <FAQSection />
        <CTASection />
      </main>
      <LandingFooter />
    </>
  );
}
