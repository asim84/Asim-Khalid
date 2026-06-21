'use client'
import { useState } from 'react'
import useSWR from 'swr'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { fetcher, formatPence, type FeeSummary, type FeeBreakdownItem } from '@/lib/api'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

const PERIODS = ['30d', '90d'] as const
type Period = (typeof PERIODS)[number]

export default function FeeBreakdown() {
  const [period, setPeriod] = useState<Period>('30d')
  const { data: summary } = useSWR<FeeSummary>(`/api/fees/summary?period=${period}`, fetcher)
  const { data: breakdown } = useSWR<FeeBreakdownItem[]>(`/api/fees/breakdown?period=${period}`, fetcher)

  const pieData = (breakdown ?? []).map((item) => ({
    name: item.fee_type,
    value: item.total_pence,
  }))

  const largest = (breakdown ?? []).reduce(
    (max, item) => (item.total_pence > (max?.total_pence ?? 0) ? item : max),
    null as FeeBreakdownItem | null
  )

  return (
    <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-100">Fee Breakdown</h2>
        <div className="flex gap-1">
          {PERIODS.map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-2 py-1 rounded text-xs font-medium transition-colors ${
                period === p ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-slate-700'
              }`}
            >
              {p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} strokeWidth={0}>
            {pieData.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 8 }}
            formatter={(value: number) => [formatPence(value), '']}
          />
          <Legend
            formatter={(value) => <span style={{ color: '#94a3b8', fontSize: 11 }}>{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>

      <div className="mt-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Total Fees</span>
          <span className="text-slate-100 font-semibold">{formatPence(summary?.total_fees_pence ?? 0)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Fee % of Revenue</span>
          <span className={`font-semibold ${(summary?.fee_percentage ?? 0) > 25 ? 'text-red-400' : 'text-slate-100'}`}>
            {summary?.fee_percentage?.toFixed(1) ?? '0.0'}%
          </span>
        </div>
        {largest && (
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Largest Fee Type</span>
            <span className="text-slate-300 text-xs text-right max-w-[140px] truncate">{largest.fee_type}</span>
          </div>
        )}
      </div>
    </div>
  )
}
