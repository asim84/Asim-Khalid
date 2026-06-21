'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { BarChart3, TrendingUp, Package, Receipt, Lightbulb } from 'lucide-react'
import useSWR from 'swr'
import { fetcher } from '@/lib/api'

const navItems = [
  { label: 'Overview', href: '/', icon: BarChart3 },
  { label: 'Sales', href: '/sales', icon: TrendingUp },
  { label: 'Inventory', href: '/inventory', icon: Package },
  { label: 'Fees', href: '/fees', icon: Receipt },
  { label: 'Insights', href: '/insights', icon: Lightbulb },
]

export default function Navbar() {
  const pathname = usePathname()
  const { data: health } = useSWR('/api/health', fetcher, { refreshInterval: 60000 })

  const lastSync = health?.last_sync
    ? new Date(health.last_sync).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
    : 'Never'

  return (
    <nav className="w-64 flex-shrink-0 flex flex-col" style={{ background: '#0f172a', borderRight: '1px solid #1e293b' }}>
      <div className="p-6">
        <span className="text-2xl font-bold text-blue-500">BizAI</span>
        <p className="text-xs text-slate-500 mt-1">E-commerce Intelligence</p>
      </div>
      <ul className="flex-1 px-3 space-y-1">
        {navItems.map(({ label, href, icon: Icon }) => {
          const active = pathname === href
          return (
            <li key={href}>
              <Link
                href={href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  active
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <Icon size={18} />
                {label}
              </Link>
            </li>
          )
        })}
      </ul>
      <div className="p-4 border-t border-slate-800">
        <p className="text-xs text-slate-500">Last sync</p>
        <p className="text-xs text-slate-400 font-medium">{lastSync}</p>
      </div>
    </nav>
  )
}
