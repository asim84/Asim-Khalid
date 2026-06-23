import LandingNavbar from '@/components/LandingNavbar'
import HeroSection from '@/components/HeroSection'
import FeaturesSection from '@/components/FeaturesSection'
import TrustSection from '@/components/TrustSection'
import CtaSection from '@/components/CtaSection'

export default function LandingPage() {
  return (
    <>
      <LandingNavbar />
      <main>
        <HeroSection />
        <FeaturesSection />
        <TrustSection />
        <CtaSection />
      </main>
      <footer className="border-t border-slate-800 py-8 text-center text-sm text-slate-500">
        © {new Date().getFullYear()} SentinelAI. All rights reserved.
      </footer>
    </>
  )
}
