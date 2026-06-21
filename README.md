# BizAI — E-commerce Intelligence Platform

BizAI is a full-stack business intelligence system for Amazon and Linnworks sellers. It ingests data from Dropbox (Linnworks CSV exports) and the Amazon SP-API, stores everything in SQLite, runs automated AI analysis via Claude, and presents it in a live Next.js dashboard.

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                      Next.js Frontend                  │
│  Dashboard │ SalesChart │ InventoryTable │ AIInsights   │
└───────────────────────┬────────────────────────────────┘
                        │  /api/* (rewritten to :8000)
┌───────────────────────▼────────────────────────────────┐
│                  FastAPI Backend (:8000)                │
│  /api/sales   /api/inventory   /api/fees   /api/insights│
├────────────────────────────────────────────────────────┤
│  APScheduler (sync every N minutes)                    │
│  ├── Dropbox → Linnworks CSV parser → SQLite           │
│  ├── Amazon SP-API connector → SQLite                  │
│  └── Claude AI Analyzer → AIInsight records            │
├────────────────────────────────────────────────────────┤
│  SQLite database (bizai.db)                            │
│  Orders │ InventoryItems │ FeeRecords │ AIInsights      │
└────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- A Dropbox app with an access token
- Amazon SP-API developer account (optional — app works with seed data)
- Anthropic API key (for AI insights)

---

## Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Populate with demo data (recommended for first run)
python seed_data.py

# Start the API server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

---

## Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`.

---

## Connecting Linnworks

1. In Linnworks, go to **Settings → Macros & Scripts** or use the Linnworks API to schedule exports.
2. Export **Open Orders** and **My Inventory** as CSV files.
3. Upload the CSV files to the Dropbox folder specified in `DROPBOX_LINNWORKS_FOLDER` (default: `/Linnworks/exports`).
4. BizAI will automatically detect and import them on the next sync cycle.

**Supported Linnworks export formats:**
- Orders export: must include columns for Order ID, SKU, Quantity, Total, Order Date
- Inventory export: must include SKU, Stock Level, Cost Price, Retail Price

---

## Amazon SP-API Credentials

1. Go to [Seller Central → Apps & Services → Develop Apps](https://sellercentral.amazon.co.uk/apps/develop)
2. Register as a developer and create a new app
3. Generate a **refresh token** using the SP-API OAuth flow (LWA)
4. Copy `Client ID`, `Client Secret`, and `Refresh Token` to your `.env` file
5. Set `AMAZON_MARKETPLACE_ID` to `A1F83G8C2ARO7P` for Amazon UK

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DROPBOX_ACCESS_TOKEN` | Dropbox app access token | Required |
| `DROPBOX_LINNWORKS_FOLDER` | Dropbox path to Linnworks exports | `/Linnworks/exports` |
| `AMAZON_REFRESH_TOKEN` | Amazon SP-API LWA refresh token | Optional |
| `AMAZON_CLIENT_ID` | Amazon SP-API client ID | Optional |
| `AMAZON_CLIENT_SECRET` | Amazon SP-API client secret | Optional |
| `AMAZON_MARKETPLACE_ID` | Amazon marketplace ID | `A1F83G8C2ARO7P` (UK) |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | Required for AI insights |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./bizai.db` |
| `SYNC_INTERVAL_MINUTES` | How often to sync data | `60` |

---

## Folder Structure

```
bizai/
├── backend/
│   ├── analysis/
│   │   └── ai_analyzer.py      # Claude-powered business analysis
│   ├── connectors/
│   │   ├── amazon_connector.py # Amazon SP-API client
│   │   └── dropbox_connector.py# Dropbox file sync
│   ├── parsers/
│   │   └── linnworks_parser.py # Linnworks CSV parser
│   ├── routers/
│   │   ├── fees.py             # Fee analytics endpoints
│   │   ├── insights.py         # AI insights + sync endpoints
│   │   ├── inventory.py        # Inventory status endpoints
│   │   └── sales.py            # Sales analytics endpoints
│   ├── database.py             # SQLAlchemy models
│   ├── main.py                 # FastAPI application
│   ├── scheduler.py            # APScheduler background sync
│   ├── seed_data.py            # Demo data generator
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/                # Next.js app router
│       ├── components/
│       │   ├── AIInsights.tsx  # AI insights card list
│       │   ├── Dashboard.tsx   # Main dashboard layout
│       │   ├── FeeBreakdown.tsx# Pie chart + fee stats
│       │   ├── InventoryTable.tsx # Inventory with status
│       │   ├── MetricCard.tsx  # KPI metric card
│       │   ├── Navbar.tsx      # Left sidebar navigation
│       │   └── SalesChart.tsx  # Revenue + orders chart
│       └── lib/
│           └── api.ts          # Typed API client + helpers
└── README.md
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/health` | Health check |
| GET | `/api/sales/summary?period=30d` | Sales KPIs |
| GET | `/api/sales/chart?period=30d` | Daily revenue/orders |
| GET | `/api/sales/by_sku?period=30d` | Sales by SKU |
| GET | `/api/inventory/` | All inventory items |
| GET | `/api/inventory/alerts` | Low stock alerts |
| GET | `/api/fees/summary?period=30d` | Fee totals |
| GET | `/api/fees/breakdown` | Fee by type |
| GET | `/api/insights/` | AI insights |
| POST | `/api/insights/{id}/read` | Mark insight read |
| POST | `/api/insights/sync/trigger` | Trigger manual sync |
| GET | `/api/insights/sync/status` | Sync log |
