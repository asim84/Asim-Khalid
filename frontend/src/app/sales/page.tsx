'use client'
import useSWR from 'swr'
import { useState } from 'react'
import MetricCard from '@/components/MetricCard'
import SalesChart from '@/components/SalesChart'
import { fetcher, formatPence, formatPct, type SalesSummary, type SKUSale } from '@/lib/api'

const PERIODS = [
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
  { label: '90D', value: '90d' },
]

export default function SalesPage() {
  const [period, setPeriod] = useState('30d')
  const days = period === '7d' ? 7 : period === '30d' ? 30 : 90

  const { data: summary, isLoading: summaryLoading } = useSWR<SalesSummary>(
    `/api/sales/summary?period=${period}`,
    fetcher
  )
  const { data: bySku, isLoading: skuLoading } = useSWR<SKUSale[]>(
    `/api/sales/by_sku?days=${days}`,
    fetcher
  )

  return (
    <div className="space-y-6 pb-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Sales</h1>
        <div className="flex gap-1">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                period === p.value ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard
          title={`Revenue (${period.toUpperCase()})`}
          value={summary ? formatPence(summary.total_revenue_pence) : '—'}
          change={summary?.revenue_change_pct}
          changeLabel="vs prev period"
          loading={summaryLoading}
        />
        <MetricCard
          title={`Orders (${period.toUpperCase()})`}
          value={summary ? summary.total_orders.toLocaleString() : '—'}
          change={summary?.orders_change_pct}
          changeLabel="vs prev period"
          loading={summaryLoading}
        />
        <MetricCard
          title={`Units Sold (${period.toUpperCase()})`}
          value={summary ? summary.total_units.toLocaleString() : '—'}
          loading={summaryLoading}
        />
        <MetricCard
          title="Avg Order Value"
          value={summary ? formatPence(summary.avg_order_value_pence) : '—'}
          loading={summaryLoading}
        />
      </div>

      <SalesChart />

      <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Sales by SKU</h2>
        {skuLoading ? (
          <div className="space-y-2">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-10 rounded bg-slate-700 animate-pulse" />
            ))}
          </div>
        ) : !bySku?.length ? (
          <p className="text-slate-500 text-sm text-center py-8">No sales data yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-500 border-b border-slate-700">
                  <th className="pb-2 pr-4">#</th>
                  <th className="pb-2 pr-4">SKU</th>
                  <th className="pb-2 pr-4">Title</th>
                  <th className="pb-2 pr-4 text-right">Revenue</th>
                  <th className="pb-2 text-right">Units</th>
                </tr>
              </thead>
              <tbody>
                {bySku.map((row) => (
                  <tr key={row.sku} className="border-b border-slate-800 hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 pr-4 text-slate-500 text-xs">{row.rank}</td>
                    <td className="py-2.5 pr-4 font-mono text-xs text-slate-300">{row.sku}</td>
                    <td className="py-2.5 pr-4 text-slate-300 max-w-xs truncate">{row.title}</td>
                    <td className="py-2.5 pr-4 text-right text-slate-200 font-semibold">{formatPence(row.revenue_pence)}</td>
                    <td className="py-2.5 text-right text-slate-400">{row.units.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
