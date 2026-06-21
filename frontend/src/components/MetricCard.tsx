'use client'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface Props {
  title: string
  value: string
  change?: number
  changeLabel?: string
  loading?: boolean
}

export default function MetricCard({ title, value, change, changeLabel, loading }: Props) {
  const isPositive = (change ?? 0) > 0
  const isNegative = (change ?? 0) < 0

  if (loading) {
    return (
      <div className="rounded-xl p-6 animate-pulse" style={{ background: '#1e293b' }}>
        <div className="h-4 w-24 bg-slate-700 rounded mb-4" />
        <div className="h-8 w-32 bg-slate-700 rounded mb-3" />
        <div className="h-4 w-20 bg-slate-700 rounded" />
      </div>
    )
  }

  return (
    <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
      <p className="text-sm text-slate-400 mb-1">{title}</p>
      <p className="text-3xl font-bold text-white mb-2">{value}</p>
      {change !== undefined && (
        <div className={`flex items-center gap-1 text-sm ${isPositive ? 'text-green-400' : isNegative ? 'text-red-400' : 'text-slate-400'}`}>
          {isPositive ? <TrendingUp size={14} /> : isNegative ? <TrendingDown size={14} /> : <Minus size={14} />}
          <span>{change > 0 ? '+' : ''}{change.toFixed(1)}%</span>
          {changeLabel && <span className="text-slate-500 ml-1">{changeLabel}</span>}
        </div>
      )}
    </div>
  )
}
