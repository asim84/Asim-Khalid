export const fetcher = (url: string) => fetch(url).then(r => r.json())

export function formatPence(pence: number): string {
  return new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP' }).format(pence / 100)
}

export function formatPct(value: number): string {
  return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`
}

export interface SalesSummary {
  total_revenue_pence: number
  total_orders: number
  total_units: number
  avg_order_value_pence: number
  revenue_change_pct: number
  orders_change_pct: number
  period_days: number
}

export interface DailyStat {
  date: string
  revenue_pence: number
  orders: number
  units: number
}

export interface SKUSale {
  sku: string
  title: string
  revenue_pence: number
  units: number
  rank: number
}

export interface InventoryItem {
  id: number
  sku: string
  asin: string | null
  title: string
  quantity_available: number
  quantity_inbound: number
  quantity_reserved: number
  reorder_point: number
  days_of_cover: number
  sell_price_pence: number
  cost_price_pence: number
  status: 'ok' | 'warning' | 'critical'
  last_updated: string
}

export interface FeeSummary {
  total_fees_pence: number
  referral_fees_pence: number
  fba_fees_pence: number
  other_fees_pence: number
  fee_percentage: number
  period_days: number
}

export interface FeeBreakdownItem {
  fee_type: string
  total_pence: number
  percentage: number
}

export interface AIInsight {
  id: number
  insight_type: string
  severity: 'info' | 'warning' | 'critical'
  title: string
  description: string
  affected_skus: string | null
  generated_at: string
  is_read: boolean
}

export async function markInsightRead(id: number) {
  await fetch(`/api/insights/${id}/read`, { method: 'POST' })
}

export async function triggerSync() {
  await fetch('/api/insights/sync/trigger', { method: 'POST' })
}
