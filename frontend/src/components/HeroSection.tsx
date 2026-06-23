import Link from 'next/link'
import { ArrowRight, ShieldCheck } from 'lucide-react'

export default function HeroSection() {
  return (
    <section className="pt-36 pb-24 px-6 text-center">
      <div className="max-w-4xl mx-auto">
        <span className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-blue-400 bg-blue-950 border border-blue-800 rounded-full px-4 py-1.5 mb-6">
          <ShieldCheck size={14} />
          AI-Powered Threat Detection
        </span>
        <h1 className="text-5xl sm:text-6xl font-extrabold text-white leading-tight mb-6">
          Stop threats before{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
            they become breaches
          </span>
        </h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
          SentinelAI continuously monitors your infrastructure, detects anomalies in real time,
          and autonomously responds to threats — so your team can focus on what matters.
        </p>
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="#cta"
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold px-7 py-3 rounded-xl transition-colors text-sm"
          >
            Start free trial <ArrowRight size={16} />
          </Link>
          <Link
            href="#features"
            className="text-sm text-slate-300 hover:text-white border border-slate-700 hover:border-slate-500 px-7 py-3 rounded-xl transition-colors"
          >
            See how it works
          </Link>
        </div>
        <p className="mt-6 text-xs text-slate-600">No credit card required · SOC 2 Type II certified · GDPR compliant</p>
      </div>
    </section>
  )
}
