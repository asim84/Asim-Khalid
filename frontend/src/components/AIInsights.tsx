'use client'
import { useState } from 'react'
import useSWR, { useSWRConfig } from 'swr'
import { RefreshCw, CheckCircle } from 'lucide-react'
import { fetcher, markInsightRead, triggerSync, type AIInsight } from '@/lib/api'

const severityBorder: Record<string, string> = {
  critical: 'border-red-500',
  warning: 'border-amber-500',
  info: 'border-blue-500',
}

const severityBadge: Record<string, string> = {
  critical: 'bg-red-900 text-red-300',
  warning: 'bg-amber-900 text-amber-300',
  info: 'bg-blue-900 text-blue-300',
}

function timeAgo(isoStr: string): string {
  const diff = Date.now() - new Date(isoStr).getTime()
  const hours = Math.floor(diff / 3600000)
  if (hours < 1) return 'Just now'
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}

export default function AIInsights() {
  const { data, isLoading } = useSWR<AIInsight[]>('/api/insights', fetcher, { refreshInterval: 60000 })
  const { mutate } = useSWRConfig()
  const [syncing, setSyncing] = useState(false)

  async function handleMarkRead(id: number) {
    await markInsightRead(id)
    mutate('/api/insights')
  }

  async function handleSync() {
    setSyncing(true)
    await triggerSync()
    setTimeout(() => {
      setSyncing(false)
      mutate('/api/insights')
    }, 3000)
  }

  const insights = data ?? []
  const unread = insights.filter((i) => !i.is_read)
  const read = insights.filter((i) => i.is_read)

  return (
    <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">AI Insights</h2>
          {unread.length > 0 && (
            <p className="text-xs text-slate-400 mt-0.5">{unread.length} unread</p>
          )}
        </div>
        <button
          onClick={handleSync}
          disabled={syncing}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60 transition-colors"
        >
          <RefreshCw size={12} className={syncing ? 'animate-spin' : ''} />
          {syncing ? 'Syncing…' : 'Trigger Sync'}
        </button>
      </div>

      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-24 rounded-lg bg-slate-700 animate-pulse" />
          ))}
        </div>
      ) : insights.length === 0 ? (
        <p className="text-slate-500 text-sm text-center py-8">No insights yet. Trigger a sync to generate analysis.</p>
      ) : (
        <div className="space-y-3">
          {[...unread, ...read].map((insight) => (
            <div
              key={insight.id}
              className={`rounded-lg p-4 border-l-4 transition-opacity ${severityBorder[insight.severity] ?? 'border-slate-500'} ${
                insight.is_read ? 'opacity-60' : ''
              }`}
              style={{ background: '#0f172a' }}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${severityBadge[insight.severity] ?? 'bg-slate-700 text-slate-300'}`}>
                      {insight.severity}
                    </span>
                    <span className="text-xs text-slate-500">{timeAgo(insight.generated_at)}</span>
                  </div>
                  <p className="text-sm font-semibold text-slate-200 mb-1">{insight.title}</p>
                  <p className="text-xs text-slate-400 leading-relaxed">{insight.description}</p>
                  {insight.affected_skus && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {insight.affected_skus.split(',').map((sku) => (
                        <span key={sku.trim()} className="px-1.5 py-0.5 rounded bg-slate-700 text-xs font-mono text-slate-300">
                          {sku.trim()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                {!insight.is_read && (
                  <button
                    onClick={() => handleMarkRead(insight.id)}
                    className="flex-shrink-0 text-slate-500 hover:text-green-400 transition-colors"
                    title="Mark as read"
                  >
                    <CheckCircle size={16} />
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
