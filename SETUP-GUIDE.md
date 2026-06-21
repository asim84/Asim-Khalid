# BizAI Setup Guide — Step by Step (No Technical Knowledge Needed)

This guide walks you through getting BizAI running on your computer from scratch.
Estimated time: **45–60 minutes** for the first setup.

---

## BEFORE YOU START — What You Will Need

Gather these four things before you begin:

| # | What | Where to get it | Takes how long |
|---|------|----------------|---------------|
| 1 | **Dropbox account** with a folder for Linnworks exports | You likely already have this | Instant |
| 2 | **Dropbox Access Token** | Dropbox App Console (Step 3 below) | 10 minutes |
| 3 | **Amazon SP-API credentials** | Amazon Developer Console (Step 4 below) | 20–30 minutes |
| 4 | **Anthropic API key** | console.anthropic.com | 5 minutes |

---

## PART 1 — Install the Required Software

### Step 1A — Install Python

1. Open your web browser and go to: **https://www.python.org/downloads/**
2. You will see a big yellow button saying **"Download Python 3.12.x"**

   ```
   ┌─────────────────────────────────────────────────────┐
   │  python.org/downloads                               │
   │                                                     │
   │  ┌──────────────────────────────┐                  │
   │  │  Download Python 3.12.4  ▼  │  ← Click this    │
   │  └──────────────────────────────┘                  │
   └─────────────────────────────────────────────────────┘
   ```

3. Click it. A file called `python-3.12.x.exe` will download.
4. Open that file.
5. **IMPORTANT**: On the first screen, tick the box that says **"Add Python to PATH"** at the bottom.

   ```
   ┌─────────────────────────────────────────────┐
   │  Install Python 3.12                        │
   │                                             │
   │  ○ Install Now                              │
   │  ○ Customize installation                   │
   │                                             │
   │  ☑ Add Python 3.12 to PATH  ← TICK THIS    │
   └─────────────────────────────────────────────┘
   ```

6. Click **Install Now** and wait for it to finish.

---

### Step 1B — Install Node.js

1. Go to: **https://nodejs.org/**
2. Click the green button labelled **"LTS"** (the recommended version).

   ```
   ┌────────────────────────────────────────────────────┐
   │  nodejs.org                                        │
   │                                                    │
   │  ┌──────────────┐  ┌──────────────┐               │
   │  │  20.x LTS    │  │  21.x Current│               │
   │  │  Recommended │  │              │               │
   │  │  ← Click me  │  │              │               │
   │  └──────────────┘  └──────────────┘               │
   └────────────────────────────────────────────────────┘
   ```

3. Open the downloaded file and click Next → Next → Install.
4. When done, click Finish.

---

### Step 1C — Install Git

1. Go to: **https://git-scm.com/download/win**
2. The download will start automatically.
3. Open the file and click Next through all the screens (defaults are fine).
4. Click Install, then Finish.

---

### Step 1D — Verify Everything Installed

1. Press the **Windows key** on your keyboard.
2. Type `cmd` and press Enter. A black window (Command Prompt) will open.
3. Type each line below and press Enter after each:

   ```
   python --version
   ```
   You should see: `Python 3.12.x`

   ```
   node --version
   ```
   You should see: `v20.x.x`

   ```
   git --version
   ```
   You should see: `git version 2.x.x`

   If you see these, move on. If you see an error, go back and reinstall that piece of software.

---

## PART 2 — Download the BizAI Code

1. In the Command Prompt (black window), type the following and press Enter:

   ```
   cd Desktop
   ```

2. Then type this and press Enter:

   ```
   git clone https://github.com/asim84/Asim-Khalid.git
   ```

   You will see text scrolling — that is the code downloading. Wait until you get a prompt back.

3. Then type:

   ```
   cd Asim-Khalid
   ```

   You are now inside the BizAI folder.

---

## PART 3 — Get Your Dropbox Access Token

This lets BizAI read your Linnworks export files from Dropbox automatically.

1. Go to: **https://www.dropbox.com/developers/apps**
2. Sign in with your Dropbox account.
3. Click the blue **"Create app"** button.

   ```
   ┌─────────────────────────────────────────────────────┐
   │  My apps                              + Create app  │
   │                                       ← Click here  │
   └─────────────────────────────────────────────────────┘
   ```

4. You will see a form. Fill it in:
   - **Step 1 — Choose an API**: Select **"Scoped access"**
   - **Step 2 — Choose the type of access**: Select **"Full Dropbox"**
   - **Step 3 — Name your app**: Type `BizAI-Linnworks`

   ```
   ┌──────────────────────────────────────────────────────┐
   │  Create an app                                       │
   │                                                      │
   │  1. Choose an API                                    │
   │     ● Scoped access    ← Select this                 │
   │                                                      │
   │  2. Type of access                                   │
   │     ○ App folder                                     │
   │     ● Full Dropbox     ← Select this                 │
   │                                                      │
   │  3. Name your app                                    │
   │     [ BizAI-Linnworks ]                              │
   │                                                      │
   │  [ Create app ]                                      │
   └──────────────────────────────────────────────────────┘
   ```

5. Click **"Create app"**.

6. You are now on your app's settings page. Scroll down to **"OAuth 2"** section. Click the tab labelled **"Permissions"**.

7. Tick these boxes:
   - `files.metadata.read`
   - `files.content.read`

8. Click **"Submit"**.

9. Go back to the **"Settings"** tab.

10. Scroll to **"Generated access token"** and click **"Generate"**.

    ```
    ┌──────────────────────────────────────────────────┐
    │  Generated access token                          │
    │                                                  │
    │  [ Generate ]  ← Click this                      │
    │                                                  │
    │  sl.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx      │
    │                                       [Copy]     │
    └──────────────────────────────────────────────────┘
    ```

11. A long code starting with `sl.` will appear. Click **Copy** and save it somewhere (Notepad).

12. **Set up your Dropbox folder**: In Dropbox, create a folder called `Linnworks` and inside it create a folder called `exports`. The path will be `/Linnworks/exports`. This is where you will drop your Linnworks CSV files.

---

## PART 4 — Get Your Amazon SP-API Credentials

This allows BizAI to pull your orders, inventory, and fees directly from Amazon.

> **Note**: Amazon requires you to register as a developer. This is free and is just a form. It does NOT affect your seller account.

### 4A — Register as a Developer

1. Go to: **https://sellercentral.amazon.co.uk**
2. Log in with your seller account.
3. In the top menu, go to **Apps & Services → Develop Apps**.

   ```
   ┌─────────────────────────────────────────────────────────┐
   │  Seller Central                                         │
   │  Apps & Services ▼                                      │
   │    ├── Manage Your Apps                                 │
   │    └── Develop Apps     ← Click this                    │
   └─────────────────────────────────────────────────────────┘
   ```

4. Click **"Sign up to be a developer"** and fill in the form (it asks your business name and how you will use the API — say "Internal business reporting tool for my own account").

5. Agree to the terms and submit.

### 4B — Create Your SP-API Application

1. Once registered, go back to **Apps & Services → Develop Apps**.
2. Click **"Add new app client"**.

   ```
   ┌──────────────────────────────────────────────────────────┐
   │  Developer Central                                       │
   │                                                          │
   │  [ + Add new app client ]  ← Click this                 │
   └──────────────────────────────────────────────────────────┘
   ```

3. Fill in:
   - **App name**: `BizAI`
   - **IAM ARN**: Leave blank for now (you can fill this later)
   - **Roles**: Tick:
     - `Amazon Orders` — Read only
     - `Amazon Inventory` — Read only
     - `Amazon Finances` — Read only

4. Click **Save and exit**.

5. Click **"View"** next to your new app.

6. You will see:
   - **Client ID** — copy it
   - **Client Secret** — click "Show" then copy it

### 4C — Authorise the App

1. Still on the app page, click **"Authorize"**.
2. This will ask you to log in again and approve the app.
3. After approving, you will be given a **Refresh Token** — a long code. Copy it.

   > If you get stuck on this step, Amazon has a tool called the "Selling Partner API Auth Tool" — search for it in Seller Central help.

---

## PART 5 — Get Your Anthropic API Key

This powers the AI analysis (anomaly detection, alerts, recommendations).

1. Go to: **https://console.anthropic.com/**
2. Sign up or log in.
3. Click **"API Keys"** in the left menu.

   ```
   ┌─────────────────────────────────────────────┐
   │  console.anthropic.com                      │
   │                                             │
   │  ├── Dashboard                              │
   │  ├── API Keys    ← Click this               │
   │  └── Usage                                  │
   └─────────────────────────────────────────────┘
   ```

4. Click **"Create Key"**. Give it a name like `BizAI`.
5. Copy the key that appears (starts with `sk-ant-...`). You only see it once.

---

## PART 6 — Configure BizAI with Your Credentials

1. In File Explorer, go to your Desktop → `Asim-Khalid` → `backend` folder.
2. Find the file called `.env.example`.
3. Right-click it → **Copy**, then right-click → **Paste** in the same folder.
4. Right-click the copy → **Rename** → change the name to exactly `.env` (no `.example`).
5. Right-click `.env` → **Open with** → **Notepad**.
6. Fill in each line with your credentials:

   ```
   # Dropbox — paste the sl.xxx token you copied in Step 3
   DROPBOX_ACCESS_TOKEN=sl.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # The Dropbox folder path where you save Linnworks exports
   DROPBOX_LINNWORKS_FOLDER=/Linnworks/exports

   # Amazon — paste what you got in Step 4
   AMAZON_REFRESH_TOKEN=Atzr|xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   AMAZON_CLIENT_ID=amzn1.application-oa2-client.xxxxxxxxxx
   AMAZON_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # UK marketplace ID (leave this as-is for Amazon UK)
   AMAZON_MARKETPLACE_ID=A1F83G8C2ARO7P

   # Anthropic — paste the sk-ant-xxx key you copied in Step 5
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

   # Leave these as they are
   DATABASE_URL=sqlite:///./bizai.db
   SYNC_INTERVAL_MINUTES=60
   ```

7. Save and close Notepad.

---

## PART 7 — Set Up the Backend (Python)

1. Open Command Prompt (press Windows key, type `cmd`, press Enter).
2. Navigate to the backend folder:

   ```
   cd Desktop\Asim-Khalid\backend
   ```

3. Create a virtual environment (a self-contained Python space):

   ```
   python -m venv venv
   ```

   Wait about 30 seconds.

4. Activate it:

   ```
   venv\Scripts\activate
   ```

   You will see `(venv)` appear at the start of the line — that means it worked.

   ```
   (venv) C:\Users\YourName\Desktop\Asim-Khalid\backend>
   ```

5. Install all the required Python packages:

   ```
   pip install -r requirements.txt
   ```

   This downloads about 20 packages. Wait until you see `Successfully installed...`.

6. Load in some demo data so the dashboard has something to show:

   ```
   python seed_data.py
   ```

   You should see: `Seed data created successfully!`

7. Start the backend server:

   ```
   uvicorn main:app --reload --port 8000
   ```

   You should see:

   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

   **Leave this window open.** The backend is now running.

---

## PART 8 — Set Up the Frontend (Dashboard)

1. Open a **second** Command Prompt window (important — keep the first one open).
2. Navigate to the frontend folder:

   ```
   cd Desktop\Asim-Khalid\frontend
   ```

3. Install the dashboard packages:

   ```
   npm install
   ```

   This takes 1–3 minutes. You will see a lot of text. Wait until the prompt returns.

4. Start the dashboard:

   ```
   npm run dev
   ```

   You should see:

   ```
   ▲ Next.js 14.2.3
   - Local:   http://localhost:3000
   - ready in 2.1s
   ```

5. Open your web browser and go to: **http://localhost:3000**

   You should now see the BizAI dashboard!

   ```
   ┌─────────────────────────────────────────────────────────────────┐
   │ BizAI         │  BizAI Business Intelligence                    │
   │               │                                                 │
   │ Overview      │  ┌────────────┐ ┌────────────┐ ┌────────────┐ │
   │ Sales         │  │ Revenue    │ │ Orders     │ │ Inv Alerts │ │
   │ Inventory     │  │ £24,532    │ │ 187        │ │ 3 critical │ │
   │ Fees          │  │ ▲ 12.4%   │ │ ▲ 8.1%    │ │            │ │
   │ Insights      │  └────────────┘ └────────────┘ └────────────┘ │
   │               │                                                 │
   │ Last sync:    │  [  Sales Chart — 30 days                    ] │
   │ 2 mins ago    │                                                 │
   └─────────────────────────────────────────────────────────────────┘
   ```

---

## PART 9 — Export from Linnworks and Upload to Dropbox

This is your ongoing daily/weekly routine:

### In Linnworks:

1. Log in to Linnworks.
2. Go to **Reports** in the top menu.
3. For orders: select **"Open Orders"** or **"Processed Orders"** → Export → CSV.
4. For inventory: go to **Stock Items** → Export → CSV.
5. Save the file to your computer.

### Upload to Dropbox:

1. Open your Dropbox folder on your computer (or go to dropbox.com).
2. Navigate to: `Linnworks → exports`
3. Drag and drop your exported CSV files into this folder.

BizAI checks this folder every 60 minutes and automatically picks up new files, processes them, and updates the dashboard.

### Trigger an immediate sync (optional):
- In the dashboard, click **Insights** in the left menu.
- Click the **"Trigger Sync"** button to force an immediate refresh.

---

## PART 10 — Keeping BizAI Running

Each time you want to use BizAI, you need to start two things:

**Terminal 1 — Backend:**
```
cd Desktop\Asim-Khalid\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```
cd Desktop\Asim-Khalid\frontend
npm run dev
```

Then open **http://localhost:3000** in your browser.

---

## TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Black window says `'python' is not recognized` | Go back to Step 1A and reinstall Python, making sure to tick "Add to PATH" |
| `pip install` fails with an error | Make sure you see `(venv)` at the start of the line before running pip |
| Dashboard shows blank / no data | Make sure the backend is running (Terminal 1) and check it says "running on http://127.0.0.1:8000" |
| Amazon data not pulling | Double-check your credentials in the `.env` file — no spaces around the `=` sign |
| Dropbox files not being picked up | Check the folder path in `.env` matches exactly where you put the files in Dropbox |
| AI insights not generating | Check your ANTHROPIC_API_KEY in `.env` is correct and your account has credit |

---

## GETTING HELP

If you get stuck on any step, take a screenshot of the error message you see in the black window and share it. The error message will pinpoint exactly what needs fixing.
