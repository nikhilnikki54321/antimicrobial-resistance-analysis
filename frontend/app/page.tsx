import { HeroSection } from "@/components/landing/hero-section";
import { HowItWorks } from "@/components/landing/how-it-works";

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto">
      <HeroSection />
      <HowItWorks />
    </div>
  );
}
