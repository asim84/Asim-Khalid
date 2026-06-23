'use client'
import AIInsights from '@/components/AIInsights'
import useSWR from 'swr'
import { fetcher, type AIInsight } from '@/lib/api'

export default function InsightsPage() {
  const { data } = useSWR<AIInsight[]>('/api/insights', fetcher, { refreshInterval: 60000 })

  const total = data?.length ?? 0
  const unread = data?.filter((i) => !i.is_read).length ?? 0
  const critical = data?.filter((i) => i.severity === 'critical').length ?? 0
  const warnings = data?.filter((i) => i.severity === 'warning').length ?? 0

  return (
    <div className="space-y-6 pb-6">
      <h1 className="text-2xl font-bold text-white">AI Insights</h1>

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        {[
          { title: 'Total Insights', value: total },
          { title: 'Unread', value: unread },
          { title: 'Critical', value: critical },
          { title: 'Warnings', value: warnings },
        ].map(({ title, value }) => (
          <div key={title} className="rounded-xl p-6" style={{ background: '#1e293b' }}>
            <p className="text-sm text-slate-400 mb-1">{title}</p>
            <p className="text-3xl font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      <AIInsights />
    </div>
  )
}
