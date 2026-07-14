import { Zap, Eye, Lock, BrainCircuit, Bell, Globe } from 'lucide-react'

const features = [
  {
    icon: BrainCircuit,
    title: 'AI Threat Intelligence',
    description: 'Machine learning models trained on billions of threat signals detect zero-day attacks and novel malware patterns instantly.',
  },
  {
    icon: Eye,
    title: 'Real-Time Monitoring',
    description: '24/7 visibility across your entire attack surface — cloud, endpoints, network, and SaaS — from a single pane of glass.',
  },
  {
    icon: Zap,
    title: 'Autonomous Response',
    description: 'Automated playbooks isolate compromised assets, block malicious IPs, and revoke credentials in milliseconds — not hours.',
  },
  {
    icon: Lock,
    title: 'Zero Trust Enforcement',
    description: 'Continuously verify every user, device, and workload. Adaptive access policies that tighten automatically under threat.',
  },
  {
    icon: Bell,
    title: 'Smart Alerting',
    description: 'Context-aware alerts with full kill-chain analysis. No more alert fatigue — only actionable, prioritised incidents.',
  },
  {
    icon: Globe,
    title: 'Global Threat Feed',
    description: 'Enriched with live intelligence from 10,000+ sensors worldwide. Know about emerging threats before they reach you.',
  },
]

export default function FeaturesSection() {
  return (
    <section id="features" className="py-24 px-6 border-t border-slate-800">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Everything you need to stay secure</h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            Built for security teams that move fast and can't afford to miss a thing.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="rounded-2xl border border-slate-800 p-6 hover:border-blue-800 transition-colors"
              style={{ background: '#111827' }}
            >
              <div className="w-10 h-10 rounded-lg bg-blue-950 flex items-center justify-center mb-4">
                <Icon size={20} className="text-blue-400" />
              </div>
              <h3 className="text-white font-semibold mb-2">{title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
