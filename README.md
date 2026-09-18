# 🌴 Florida Lottery Odds Tracker

> Real-time mathematical analysis, Expected Value (EV) modeling, and jackpot depletion tracking for active Florida Lottery scratch-off games.

---

## ⚡ The Problem & The Solution
Most players pick scratch-off tickets based solely on ticket art, recent wins, or printed overall odds. However:
1. Printed ticket odds reflect the game **at launch**, not its current state.
2. If all top grand prizes are already cashed in, the actual return on investment drops sharply.
3. The true statistical "Sweet Spot" occurs when a high percentage of tickets have been purchased and discarded, but a majority of the top grand prizes remain unclaimed.

**Florida Lottery Odds Tracker** automatically ingests official state catalog and tier data, recalculates prize pool depletion, and computes real-time Expected Value (EV) per ticket to surface the best statistical opportunities.

---

## 📊 Core Features & Analytics
* **Expected Value (EV) Engine:** Calculates the net statistical cash worth remaining inside every un-scratched ticket relative to its face price.
* **Depletion Tracking:** Analyzes low-to-mid tier claim volumes against published overall odds to estimate total print run size and unbought ticket counts.
* **Jackpot Monitoring:** Live tracking of remaining vs. total top-tier grand prizes.
* **Dead Jackpot & High Edge Alerts:**
  * ⚠️ **Dead Jackpot:** Immediate warning if all top grand prizes have already been cashed in.
  * 🔥 **High Edge:** Flagged when print runs exceed 65% depletion while retaining 50%+ of top prizes.
* **Mobile-First Interface:** Responsive design with electric high-contrast styling (`#65fff4` Teal, `#f465ff` Neon Pink, `#65ffa7` Mint) optimized for glanceable checks in line or on mobile devices.

---

## 🛠️ Tech Stack
* **Python 3.10+**
* **Requests & ThreadPoolExecutor:** Multi-threaded scraper fetching 165+ game tiers concurrently.
* **Pandas:** Data modeling, EV aggregation, and structured CSV/JSON exports.
* **Streamlit:** Lightweight reactive web dashboard with custom CSS overrides for responsive layouts.

---

## 🚀 Quickstart & Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/](https://github.com/)<your-username>/florida-lottery-odds-tracker.git
cd florida-lottery-odds-tracker
