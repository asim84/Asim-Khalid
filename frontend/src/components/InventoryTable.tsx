'use client'
import { useState } from 'react'
import useSWR from 'swr'
import { fetcher, type InventoryItem } from '@/lib/api'

const PAGE_SIZE = 20

const statusColors: Record<string, string> = {
  ok: 'bg-emerald-900 text-emerald-300',
  warning: 'bg-amber-900 text-amber-300',
  critical: 'bg-red-900 text-red-300',
}

export default function InventoryTable() {
  const { data, isLoading } = useSWR<InventoryItem[]>('/api/inventory', fetcher, { refreshInterval: 60000 })
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(0)

  const filtered = (data ?? []).filter(
    (item) =>
      item.sku.toLowerCase().includes(search.toLowerCase()) ||
      item.title.toLowerCase().includes(search.toLowerCase())
  )

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paged = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)

  return (
    <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-100">Inventory</h2>
        <input
          type="text"
          placeholder="Search SKU or title..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(0) }}
          className="px-3 py-1.5 rounded-lg text-sm text-slate-200 placeholder-slate-500 outline-none focus:ring-1 focus:ring-blue-500"
          style={{ background: '#0f172a', border: '1px solid #334155' }}
        />
      </div>

      {isLoading ? (
        <div className="space-y-2">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-10 rounded bg-slate-700 animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-slate-500 border-b border-slate-700">
                  <th className="pb-2 pr-4">SKU</th>
                  <th className="pb-2 pr-4">Title</th>
                  <th className="pb-2 pr-4 text-right">Available</th>
                  <th className="pb-2 pr-4 text-right">Days Cover</th>
                  <th className="pb-2 pr-4 text-right">Reorder Pt</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {paged.map((item) => (
                  <tr key={item.sku} className="border-b border-slate-800 hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 pr-4 font-mono text-xs text-slate-300">{item.sku}</td>
                    <td className="py-2.5 pr-4 text-slate-300 max-w-xs truncate">{item.title}</td>
                    <td className="py-2.5 pr-4 text-right text-slate-200">{item.quantity_available}</td>
                    <td className={`py-2.5 pr-4 text-right font-semibold ${
                      item.days_of_cover < 7 ? 'text-red-400' :
                      item.days_of_cover < 14 ? 'text-amber-400' : 'text-slate-200'
                    }`}>
                      {item.days_of_cover === 999 ? '∞' : item.days_of_cover.toFixed(1)}
                    </td>
                    <td className="py-2.5 pr-4 text-right text-slate-400">{item.reorder_point}</td>
                    <td className="py-2.5">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColors[item.status] ?? 'bg-slate-700 text-slate-300'}`}>
                        {item.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4 text-xs text-slate-400">
              <span>{filtered.length} items</span>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage((p) => Math.max(0, p - 1))}
                  disabled={page === 0}
                  className="px-2 py-1 rounded bg-slate-700 disabled:opacity-40 hover:bg-slate-600"
                >
                  Prev
                </button>
                <span className="py-1">
                  {page + 1} / {totalPages}
                </span>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                  disabled={page >= totalPages - 1}
                  className="px-2 py-1 rounded bg-slate-700 disabled:opacity-40 hover:bg-slate-600"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
