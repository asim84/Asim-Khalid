'use client'
import useSWR from 'swr'
import MetricCard from './MetricCard'
import SalesChart from './SalesChart'
import InventoryTable from './InventoryTable'
import FeeBreakdown from './FeeBreakdown'
import AIInsights from './AIInsights'
import { fetcher, formatPence, type SalesSummary, type InventoryItem, type FeeSummary } from '@/lib/api'

export default function Dashboard() {
  const { data: sales, isLoading: salesLoading } = useSWR<SalesSummary>('/api/sales/summary?period=30d', fetcher)
  const { data: inventory, isLoading: invLoading } = useSWR<InventoryItem[]>('/api/inventory/alerts', fetcher)
  const { data: fees, isLoading: feesLoading } = useSWR<FeeSummary>('/api/fees/summary?period=30d', fetcher)

  const alertCount = inventory?.length ?? 0

  return (
    <div className="space-y-6 pb-6">
      {/* Metric Cards */}
      <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <MetricCard
          title="Total Revenue (30d)"
          value={sales ? formatPence(sales.total_revenue_pence) : '—'}
          change={sales?.revenue_change_pct}
          changeLabel="vs prev period"
          loading={salesLoading}
        />
        <MetricCard
          title="Total Orders (30d)"
          value={sales ? sales.total_orders.toLocaleString() : '—'}
          change={sales?.orders_change_pct}
          changeLabel="vs prev period"
          loading={salesLoading}
        />
        <MetricCard
          title="Inventory Alerts"
          value={invLoading ? '—' : alertCount.toString()}
          changeLabel="items need attention"
          loading={invLoading}
        />
        <MetricCard
          title="Fee Rate (30d)"
          value={fees ? `${fees.fee_percentage.toFixed(1)}%` : '—'}
          changeLabel="of revenue"
          loading={feesLoading}
        />
      </div>

      {/* Sales Chart */}
      <SalesChart />

      {/* Inventory + Fee Breakdown */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2">
          <InventoryTable />
        </div>
        <div>
          <FeeBreakdown />
        </div>
      </div>

      {/* AI Insights */}
      <AIInsights />
    </div>
  )
}
