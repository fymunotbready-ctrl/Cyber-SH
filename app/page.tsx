import { AmbientBackground } from "@/components/ambient-background"
import { Navbar } from "@/components/navbar"
import { Hero } from "@/components/hero"
import { Showcase } from "@/components/showcase"
import { FeatureGrid } from "@/components/feature-grid"
import { CtaFooter } from "@/components/cta-footer"

export default function Page() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-background">
      <AmbientBackground />
      <Navbar />
      <Hero />
      <Showcase />
      <FeatureGrid />
      <CtaFooter />
    </main>
  )
}
