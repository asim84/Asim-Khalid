'use client'
import { useState } from 'react'
import useSWR from 'swr'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { fetcher, formatPence, DailyStat } from '@/lib/api'

const periods = [
  { label: '7D', value: '7d' },
  { label: '30D', value: '30d' },
  { label: '90D', value: '90d' },
]

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}

export default function SalesChart() {
  const [period, setPeriod] = useState('30d')
  const { data, isLoading } = useSWR<DailyStat[]>(`/api/sales/chart?period=${period}`, fetcher, { refreshInterval: 300000 })

  const chartData = (data || []).map(d => ({
    ...d,
    revenue_gbp: d.revenue_pence / 100,
    date_label: formatDate(d.date),
  }))

  return (
    <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-white">Revenue & Orders</h2>
        <div className="flex gap-1">
          {periods.map(p => (
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
      {isLoading ? (
        <div className="h-64 flex items-center justify-center">
          <div className="animate-spin h-8 w-8 border-2 border-blue-500 border-t-transparent rounded-full" />
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={chartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <defs>
              <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="ordGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="date_label" tick={{ fill: '#94a3b8', fontSize: 11 }} tickLine={false} />
            <YAxis yAxisId="rev" tick={{ fill: '#94a3b8', fontSize: 11 }} tickLine={false} tickFormatter={v => `£${v}`} />
            <YAxis yAxisId="ord" orientation="right" tick={{ fill: '#94a3b8', fontSize: 11 }} tickLine={false} />
            <Tooltip
              contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: 8 }}
              labelStyle={{ color: '#cbd5e1' }}
              formatter={(value: number, name: string) =>
                name === 'revenue_gbp' ? [formatPence(value * 100), 'Revenue'] : [value, 'Orders']
              }
            />
            <Legend wrapperStyle={{ paddingTop: 16, color: '#94a3b8', fontSize: 12 }} />
            <Area yAxisId="rev" type="monotone" dataKey="revenue_gbp" name="Revenue" stroke="#3b82f6" fill="url(#revGrad)" strokeWidth={2} dot={false} />
            <Area yAxisId="ord" type="monotone" dataKey="orders" name="Orders" stroke="#10b981" fill="url(#ordGrad)" strokeWidth={2} dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
