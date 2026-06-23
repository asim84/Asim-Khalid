const stats = [
  { value: '99.99%', label: 'Uptime SLA' },
  { value: '<50ms', label: 'Detection latency' },
  { value: '10B+', label: 'Threat signals/day' },
  { value: 'SOC 2', label: 'Type II certified' },
]

const testimonials = [
  {
    quote: 'SentinelAI detected a supply-chain compromise our entire team missed. The autonomous response saved us from a catastrophic breach.',
    name: 'Sarah Chen',
    role: 'CISO, FinTech Corp',
  },
  {
    quote: 'We cut our mean time to respond from 4 hours to under 3 minutes. The AI correlation engine is genuinely unlike anything else on the market.',
    name: 'Marcus Webb',
    role: 'Head of Security Ops, RetailScale',
  },
]

export default function TrustSection() {
  return (
    <section id="trust" className="py-24 px-6 border-t border-slate-800">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-8 mb-20">
          {stats.map(({ value, label }) => (
            <div key={label} className="text-center">
              <p className="text-3xl font-extrabold text-white mb-1">{value}</p>
              <p className="text-sm text-slate-500">{label}</p>
            </div>
          ))}
        </div>
        <div className="grid sm:grid-cols-2 gap-6">
          {testimonials.map(({ quote, name, role }) => (
            <blockquote
              key={name}
              className="rounded-2xl border border-slate-800 p-8"
              style={{ background: '#111827' }}
            >
              <p className="text-slate-300 leading-relaxed mb-6">&ldquo;{quote}&rdquo;</p>
              <footer>
                <p className="text-white font-semibold text-sm">{name}</p>
                <p className="text-slate-500 text-xs mt-0.5">{role}</p>
              </footer>
            </blockquote>
          ))}
        </div>
      </div>
    </section>
  )
}
