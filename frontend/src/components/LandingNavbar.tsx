'use client'
import Link from 'next/link'
import { Shield } from 'lucide-react'

export default function LandingNavbar() {
  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-slate-800 backdrop-blur-md" style={{ background: 'rgba(15,23,42,0.85)' }}>
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/landing" className="flex items-center gap-2">
          <Shield size={22} className="text-blue-500" />
          <span className="text-lg font-bold text-white">SentinelAI</span>
        </Link>
        <nav className="hidden md:flex items-center gap-8 text-sm text-slate-400">
          <Link href="#features" className="hover:text-white transition-colors">Features</Link>
          <Link href="#trust" className="hover:text-white transition-colors">Why Us</Link>
          <Link href="#cta" className="hover:text-white transition-colors">Pricing</Link>
        </nav>
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="text-sm text-slate-400 hover:text-white transition-colors px-3 py-1.5"
          >
            Sign in
          </Link>
          <Link
            href="#cta"
            className="text-sm bg-blue-600 hover:bg-blue-500 text-white px-4 py-1.5 rounded-lg transition-colors"
          >
            Get started
          </Link>
        </div>
      </div>
    </header>
  )
}
