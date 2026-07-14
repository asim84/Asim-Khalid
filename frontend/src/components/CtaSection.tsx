import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

export default function CtaSection() {
  return (
    <section id="cta" className="py-24 px-6 border-t border-slate-800">
      <div
        className="max-w-3xl mx-auto rounded-3xl border border-blue-900 p-12 text-center"
        style={{ background: 'linear-gradient(135deg, #0f1f3d 0%, #0f172a 100%)' }}
      >
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
          Ready to secure your business?
        </h2>
        <p className="text-slate-400 mb-8 max-w-lg mx-auto">
          Join hundreds of security teams protecting their infrastructure with SentinelAI.
          Start your 14-day free trial — no credit card required.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/"
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors"
          >
            Start free trial <ArrowRight size={16} />
          </Link>
          <Link
            href="/"
            className="text-sm text-slate-300 hover:text-white border border-slate-700 hover:border-slate-500 px-8 py-3 rounded-xl transition-colors"
          >
            Book a demo
          </Link>
        </div>
      </div>
    </section>
  )
}
