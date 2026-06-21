# BizAI — E-commerce Business Intelligence

Real-time dashboard for tracking sales, inventory, and fees across Amazon and Linnworks.

## What it does

- Watches Dropbox for Linnworks CSV exports (orders & inventory)
- Polls Amazon SP-API for orders, inventory, and fees
- Normalises all data into a local SQLite database
- Runs Claude AI analysis every hour to detect anomalies and generate alerts
- Serves a live Next.js dashboard with auto-refresh

## Architecture

```
Dropbox (Linnworks CSVs)
        |
        v
  Python FastAPI  ──── SQLite DB ──── Next.js Dashboard
        |                                    ^
        v                                    |
 Amazon SP-API                          REST API
        |
        v
   Claude AI (analysis)
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- Dropbox account with API access
- Amazon Seller Central account with SP-API developer access
- Anthropic API key

## Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

**To run with demo data (no real credentials needed):**
```bash
python seed_data.py
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Connecting Linnworks

1. In Linnworks, go to **Reports** and export:
   - Orders: export as CSV, name the file `orders_YYYYMMDD.csv`
   - Inventory: export as CSV, name the file `inventory_YYYYMMDD.csv`
2. Save the files to your Dropbox folder (set in `DROPBOX_LINNWORKS_FOLDER`)
3. BizAI picks them up on the next sync (hourly, or click Sync Now)

## Amazon SP-API Setup

1. Go to [Amazon Developer Central](https://developer.amazon.com)
2. Register as a developer under your Seller Central account
3. Create a new app — select **Selling Partner API**
4. Note your **Client ID** and **Client Secret**
5. Complete the OAuth flow to get your **Refresh Token**
6. Set `AMAZON_MARKETPLACE_ID`:
   - UK: `A1F83G8C2ARO7P`
   - DE: `A1PA6795UKMFR9`
   - FR: `A13V1IB3VIYZZH`

## Environment Variables

| Variable | Description |
|---|---|
| `DROPBOX_ACCESS_TOKEN` | Dropbox app access token |
| `DROPBOX_LINNWORKS_FOLDER` | Path to Linnworks exports folder in Dropbox |
| `AMAZON_REFRESH_TOKEN` | Amazon SP-API OAuth refresh token |
| `AMAZON_CLIENT_ID` | Amazon SP-API app client ID |
| `AMAZON_CLIENT_SECRET` | Amazon SP-API app client secret |
| `AMAZON_MARKETPLACE_ID` | Amazon marketplace ID (UK default) |
| `ANTHROPIC_API_KEY` | Anthropic API key for AI analysis |
| `DATABASE_URL` | SQLite path (default: `sqlite:///./bizai.db`) |
| `SYNC_INTERVAL_MINUTES` | How often to sync (default: 60) |

## Folder Structure

```
backend/
  main.py              FastAPI entry point
  scheduler.py         APScheduler sync jobs
  database.py          SQLAlchemy models
  seed_data.py         Demo data generator
  connectors/
    dropbox_connector.py
    amazon_connector.py
  parsers/
    linnworks_parser.py
  analysis/
    ai_analyzer.py
  routers/
    sales.py, inventory.py, fees.py, insights.py

frontend/
  src/app/             Next.js app router
  src/components/      Dashboard, charts, tables
  src/lib/api.ts       API client + types
```
