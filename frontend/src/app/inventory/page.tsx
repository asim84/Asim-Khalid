'use client'
import useSWR from 'swr'
import MetricCard from '@/components/MetricCard'
import InventoryTable from '@/components/InventoryTable'
import { fetcher, type InventoryItem } from '@/lib/api'

export default function InventoryPage() {
  const { data, isLoading } = useSWR<InventoryItem[]>('/api/inventory', fetcher, { refreshInterval: 60000 })
  const { data: alerts, isLoading: alertsLoading } = useSWR<InventoryItem[]>('/api/inventory/alerts', fetcher, { refreshInterval: 60000 })

  const total = data?.length ?? 0
  const critical = data?.filter((i) => i.status === 'critical').length ?? 0
  const warning = data?.filter((i) => i.status === 'warning').length ?? 0
  const ok = data?.filter((i) => i.status === 'ok').length ?? 0

  return (
    <div className="space-y-6 pb-6">
      <h1 className="text-2xl font-bold text-white">Inventory</h1>

      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard title="Total SKUs" value={isLoading ? '—' : total.toString()} loading={isLoading} />
        <MetricCard title="Critical" value={isLoading ? '—' : critical.toString()} loading={isLoading} />
        <MetricCard title="Warning" value={isLoading ? '—' : warning.toString()} loading={isLoading} />
        <MetricCard title="Healthy" value={isLoading ? '—' : ok.toString()} loading={isLoading} />
      </div>

      {alerts && alerts.length > 0 && (
        <div className="rounded-xl p-6" style={{ background: '#1e293b' }}>
          <h2 className="text-lg font-semibold text-slate-100 mb-4">
            Alerts
            <span className="ml-2 px-2 py-0.5 rounded bg-red-900 text-red-300 text-xs font-medium">{alerts.length}</span>
          </h2>
          <div className="space-y-2">
            {alerts.map((item) => (
              <div
                key={item.sku}
                className={`flex items-center justify-between px-4 py-3 rounded-lg ${
                  item.status === 'critical' ? 'bg-red-950 border border-red-800' : 'bg-amber-950 border border-amber-800'
                }`}
              >
                <div>
                  <span className="font-mono text-xs text-slate-300 mr-3">{item.sku}</span>
                  <span className="text-sm text-slate-300 truncate">{item.title}</span>
                </div>
                <div className="text-right text-xs flex-shrink-0 ml-4">
                  <span className={item.status === 'critical' ? 'text-red-300' : 'text-amber-300'}>
                    {item.quantity_available} units · {item.days_of_cover === 999 ? '∞' : `${item.days_of_cover.toFixed(1)}d`} cover
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <InventoryTable />
    </div>
  )
}
