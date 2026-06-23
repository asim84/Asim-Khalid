'use client'
import { useState } from 'react'
import useSWR from 'swr'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import MetricCard from '@/components/MetricCard'
import FeeBreakdown from '@/components/FeeBreakdown'
import { fetcher, formatPence, type FeeSummary, type FeeBreakdownItem } from '@/lib/api'

const PERIODS = ['30d', '90d'] as const
type Period = (typeof PERIODS)[number]

export default function FeesPage() {
  const [period, setPeriod] = useState<Period>('30d')

  const { data: summary, isLoading } = useSWR<FeeSummary>(`/api/fees/summary?period=${period}`, fetcher)
  const { data: breakdown } = useSWR<FeeBreakdownItem[]>(`/api/fees/breakdown?period=${period}`, fetcher)

  const barData = (breakdown ?? []).map((item) => ({
    name: item.fee_type,
    value: item.total_pence / 100,
    pct: item.percentage,
  }))

  return (
    <div className="space-y-6 pb-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Fees</h1>
        <div className="flex gap-1">
          {PERIODS.map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
                period === p ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'
              }`}
            >
              {p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard
          title="Total Fees"
          value={summary ? formatPence(summary.total_fees_pence) : '—'}
          loading={isLoading}
        />
        <MetricCard
          title="Referral Fees"
          value={summary ? formatPence(summary.referral_fees_pence) : '—'}
          loading={isLoading}
        />
        <MetricCard
          title="FBA Fees"
          value={summary ? formatPence(summary.fba_fees_pence) : '—'}
          loading={isLoading}
        />
        <MetricCard
          title="Fee Rate"
          value={summary ? `${summary.fee_percentage.toFixed(1)}%` : '—'}
          changeLabel="of revenue"
          loading={isLoading}
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Fee Types</h2>
          {!barData.length ? (
            <p className="text-slate-500 text-sm text-center py-12">No fee data yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={barData} margin={{ top: 5, right: 20, left: 10, bottom: 60 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis
                  dataKey="name"
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  tickLine={false}
                  angle={-35}
                  textAnchor="end"
                  interval={0}
                />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} tickLine={false} tickFormatter={(v) => `£${v}`} />
                <Tooltip
                  contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 8 }}
                  formatter={(value: number, _: string, entry: { payload: { pct: number } }) => [
                    `£${value.toFixed(2)} (${entry.payload.pct.toFixed(1)}%)`,
                    'Amount',
                  ]}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <FeeBreakdown />
      </div>

      {breakdown && breakdown.length > 0 && (
        <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Fee Detail</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-slate-500 border-b border-slate-700">
                <th className="pb-2 pr-4">Fee Type</th>
                <th className="pb-2 pr-4 text-right">Amount</th>
                <th className="pb-2 text-right">% of Fees</th>
              </tr>
            </thead>
            <tbody>
              {breakdown.map((item) => (
                <tr key={item.fee_type} className="border-b border-slate-800 hover:bg-slate-800/40 transition-colors">
                  <td className="py-2.5 pr-4 text-slate-300">{item.fee_type}</td>
                  <td className="py-2.5 pr-4 text-right text-slate-200 font-semibold">{formatPence(item.total_pence)}</td>
                  <td className="py-2.5 text-right text-slate-400">{item.percentage.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
