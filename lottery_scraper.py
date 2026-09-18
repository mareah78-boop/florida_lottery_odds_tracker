import requests
import json
import re
import pandas as pd
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Origin": "https://floridalottery.com",
    "Referer": "https://floridalottery.com/",
    "X-Partner": "web",
    "Accept": "application/json, text/plain, */*"
}

CATALOG_URL = "https://floridalottery.com/content/flalottery-web/us/en/games/scratch-offs.scratch-offs.json"
DETAIL_URL = "https://apim-website-prod-eastus.azure-api.net/scratchgamesapp/getscratchinfo"

session = requests.Session()
session.headers.update(HEADERS)

def parse_currency(val_str):
    """Converts strings like '$2,000,000' or '$1,000/WK' into a numeric float."""
    if not val_str:
        return 0.0
    cleaned = re.sub(r"[^\d.]", "", str(val_str))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def fetch_catalog():
    print("[1/3] Fetching 165 catalog entries...")
    res = session.get(CATALOG_URL, timeout=10)
    if res.status_code != 200:
        print(f"Catalog fetch failed: HTTP {res.status_code}")
        return []
    return res.json().get("data", [])

def parse_game_details(game_meta):
    gid = str(game_meta.get("id", "")).strip()
    name = game_meta.get("name", "Unknown")
    price = game_meta.get("price", 0)
    top_prize_catalog = game_meta.get("topPrize", "")

    url = f"{DETAIL_URL}?id={gid}"
    raw_data = None
    try:
        res = session.get(url, timeout=10)
        if res.status_code == 200:
            raw_data = res.json()
    except Exception:
        pass

    data = {}
    if isinstance(raw_data, list) and raw_data and isinstance(raw_data[0], dict):
        data = raw_data[0]
    elif isinstance(raw_data, dict):
        data = raw_data

    tiers = data.get("OddsTiers", [])
    has_active_tiers = isinstance(tiers, list) and len(tiers) > 0

    if has_active_tiers:
        overall_odds_raw = data.get("OverallOdds", 0)
        try:
            overall_odds = float(overall_odds_raw)
        except (ValueError, TypeError):
            overall_odds = 0.0

        total_winners = 0
        rem_winners = 0
        total_remaining_cash_pool = 0.0

        for tier in tiers:
            try:
                tot = int(tier.get("TotalPrizes", 0))
                rem = int(tier.get("PrizesRemaining", 0))
            except (ValueError, TypeError):
                tot, rem = 0, 0

            total_winners += tot
            rem_winners += rem

            prize_val = parse_currency(tier.get("PrizeAmount", 0))
            total_remaining_cash_pool += (prize_val * rem)

        top_tier = tiers[0]
        try:
            total_top = int(top_tier.get("TotalPrizes", 0))
            rem_top = int(top_tier.get("PrizesRemaining", 0))
        except (ValueError, TypeError):
            total_top, rem_top = 0, 0

        top_pct_rem = round((rem_top / total_top * 100), 2) if total_top > 0 else 0.0

        # Run-size & sales estimation
        est_total_tickets = int(round(total_winners * overall_odds)) if overall_odds > 0 else 0
        est_rem_tickets = int(round(rem_winners * overall_odds)) if overall_odds > 0 else 0
        est_tickets_sold = max(0, est_total_tickets - est_rem_tickets)
        pct_sold = round((est_tickets_sold / est_total_tickets * 100), 2) if est_total_tickets > 0 else 0.0

        # Expected Value (Cash EV per ticket)
        expected_value = round((total_remaining_cash_pool / est_rem_tickets), 2) if est_rem_tickets > 0 else 0.0

        return {
            "game_id": gid,
            "game_name": data.get("GameName") or name,
            "status": "ACTIVE",
            "ticket_price": data.get("TicketPrice") or price,
            "overall_odds": overall_odds,
            "top_prize_amount": str(top_tier.get("PrizeAmount", top_prize_catalog)).strip(),
            "top_prizes_remaining": rem_top,
            "top_prizes_total": total_top,
            "top_prize_percent_remaining": top_pct_rem,
            "est_tickets_remaining": est_rem_tickets,
            "est_tickets_total": est_total_tickets,
            "percent_sold": pct_sold,
            "expected_value": expected_value,
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        return {
            "game_id": gid,
            "game_name": name,
            "status": "ENDED / RETIRED",
            "ticket_price": price,
            "overall_odds": 0.0,
            "top_prize_amount": str(top_prize_catalog).strip(),
            "top_prizes_remaining": 0,
            "top_prizes_total": 0,
            "top_prize_percent_remaining": 0.0,
            "est_tickets_remaining": 0,
            "est_tickets_total": 0,
            "percent_sold": 100.0,
            "expected_value": 0.0,
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }

def run_pipeline():
    catalog = fetch_catalog()
    if not catalog:
        print("No catalog records found.")
        return

    total = len(catalog)
    print(f"[2/3] Extracting metrics across all {total} games...")
    records = []

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(parse_game_details, item) for item in catalog]
        completed = 0
        for f in as_completed(futures):
            completed += 1
            rec = f.result()
            if rec:
                records.append(rec)
            print(f"  Processed {completed}/{total} games...", end="\r")

    print(f"\nSuccessfully collected {len(records)} games.")

    print("[3/3] Exporting files...")
    df = pd.DataFrame(records)
    if not df.empty:
        df["ticket_price"] = pd.to_numeric(df["ticket_price"], errors="coerce").fillna(0)
        df = df.sort_values(
            by=["status", "expected_value", "top_prize_percent_remaining"], 
            ascending=[True, False, False]
        )
        df.to_csv("scratch_games_summary.csv", index=False)
        df.to_json("scratch_games_summary.json", orient="records", indent=2)
        
        active_df = df[df["status"] == "ACTIVE"]
        print(f"\nPipeline Done: {len(df)} total games written to CSV & JSON.")
        print(f"-> {len(active_df)} ACTIVE | {len(df[df['status'] == 'ENDED / RETIRED'])} ENDED / RETIRED\n")
        
        print("Top 5 Games Ranked by Expected Value (EV):")
        cols = ["game_id", "game_name", "ticket_price", "expected_value", "percent_sold", "top_prizes_remaining"]
        print(active_df[cols].head(5).to_string(index=False))

if __name__ == "__main__":
    run_pipeline()