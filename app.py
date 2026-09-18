import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Florida Lottery Odds Tracker",
    page_icon="🌴",
    layout="centered"
)

# Custom High-Impact Styling (#65fff4 Cyan, #f465ff Hot Pink, #65ffa7 Mint)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Inter:wght@700;800;900&display=swap');

    /* Global Base Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        background-color: #0b0f17 !important;
        color: #f1f5f9 !important;
    }

    /* Hero Header */
    .hero-title {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 2.35rem !important;
        font-weight: 900 !important;
        color: #65fff4 !important;
        text-shadow: 0 0 20px rgba(101, 255, 244, 0.45);
        letter-spacing: 0.8px;
        margin-bottom: 4px;
        text-transform: uppercase;
    }
    .hero-subtitle {
        font-family: 'Montserrat', sans-serif !important;
        color: #65bdff !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        margin-bottom: 22px;
        letter-spacing: 0.3px;
    }

    /* Standout Buyer's Guide Expander */
    div[data-testid="stExpander"]:has(.strategy-guide-marker) summary,
    div[data-testid="stExpander"]:first-of-type summary {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 900 !important;
        color: #65fff4 !important;
        background: linear-gradient(180deg, #162234 0%, #101926 100%) !important;
        border: 2px solid #65fff4 !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        box-shadow: 0 0 15px rgba(101, 255, 244, 0.25) !important;
        letter-spacing: 0.5px !important;
    }
    div[data-testid="stExpander"]:has(.strategy-guide-marker) summary:hover,
    div[data-testid="stExpander"]:first-of-type summary:hover {
        background-color: #1a293e !important;
        color: #ffffff !important;
    }

    /* Standard Deep Dive Expanders */
    div[data-testid="stExpander"] summary {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 900 !important;
        color: #65fff4 !important;
        background-color: #121a28 !important;
        border: 2px solid #1f3554 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    div[data-testid="stExpander"] summary svg {
        fill: #65fff4 !important;
        transform: scale(1.2) !important;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #0c121c !important;
        border: 2px solid #1f3554 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 18px !important;
        color: #e2e8f0 !important;
    }

    /* Filter Labels */
    div[data-testid="stCheckbox"] label p,
    div[data-testid="stSelectbox"] label p {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 900 !important;
        color: #65fff4 !important;
        letter-spacing: 0.4px !important;
    }
    div[data-baseweb="select"] div {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
    }

    /* Card Header Bar */
    .game-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 18px;
        margin-bottom: 10px;
    }
    .game-title-text {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        letter-spacing: 0.3px;
    }
    .ticket-badge {
        font-family: 'Montserrat', sans-serif !important;
        background: #f465ff !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        padding: 6px 18px !important;
        border-radius: 25px !important;
        box-shadow: 0 0 16px rgba(244, 101, 255, 0.6) !important;
        border: 2px solid #ffffff !important;
        display: inline-block !important;
    }

    /* Custom Metric Tiles Container */
    .metric-tiles-row {
        display: flex;
        gap: 10px;
        margin-bottom: 12px;
    }
    .metric-tile {
        flex: 1;
        background: #121a28;
        border: 2px solid #1f3554;
        border-radius: 12px;
        padding: 12px 6px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .metric-tile:hover {
        border-color: #65fff4;
        transform: translateY(-2px);
    }
    .metric-tile-label {
        font-family: 'Montserrat', sans-serif;
        color: #65fff4;
        font-size: 0.84rem;
        font-weight: 900;
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }
    .metric-tile-val {
        font-family: 'Montserrat', sans-serif;
        color: #ffffff;
        font-size: 1.55rem;
        font-weight: 900;
        margin-top: 4px;
        letter-spacing: 0.3px;
    }

    /* Strategy Banners */
    .edge-alert {
        background-color: rgba(101, 255, 167, 0.15);
        border-left: 6px solid #65ffa7;
        color: #e6ffe6;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 1.0rem;
        font-weight: 900;
        margin-top: 12px;
    }
    .avoid-alert {
        background-color: rgba(255, 101, 112, 0.15);
        border-left: 6px solid #ff6570;
        color: #ffe6f0;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 1.0rem;
        font-weight: 900;
        margin-top: 12px;
    }

    hr {
        border-color: #192333 !important;
        border-width: 1.5px !important;
        margin: 22px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "scratch_games_summary.csv"

@st.cache_data(ttl=600)
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILE)
    df["ticket_price"] = pd.to_numeric(df["ticket_price"], errors="coerce").fillna(0).astype(int)
    df["expected_value"] = pd.to_numeric(df["expected_value"], errors="coerce").fillna(0.0)
    df["percent_sold"] = pd.to_numeric(df["percent_sold"], errors="coerce").fillna(0.0)
    df["top_prize_percent_remaining"] = pd.to_numeric(df["top_prize_percent_remaining"], errors="coerce").fillna(0.0)
    return df

df = load_data()

# --- Header Section ---
st.markdown('<div class="hero-title">🌴 FLORIDA LOTTERY ODDS TRACKER</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Real-Time Scratch-Off Analytics, Expected Value & Jackpot Intel</div>', unsafe_allow_html=True)

# --- Standout Strategy Guide Expander ---
with st.expander("💡 HOW TO READ THE NUMBERS (BUYER'S GUIDE)", expanded=False):
    st.markdown("""
    <div class="strategy-guide-marker" style="font-size: 1.05rem; line-height: 1.7; color: #f1f5f9; font-weight: 800;">
        <p><b style="color: #65ffa7; font-weight: 900;">🎯 THE SWEET SPOT:</b> High % Sold + High Top Prizes Left.<br>
        When millions of cards have already been bought and cleared out, but the top jackpots haven't been hit yet, your odds improve significantly.</p>
        <hr style="border-color: #1f3554; margin: 12px 0;">
        <p><b style="color: #65fff4; font-weight: 900;">EXPECTED VALUE (EV):</b> The statistical cash worth of an un-scratched card right now. Compare tickets of the <b style="color: #ffffff;">same price</b> to find the game offering the highest cash return per dollar.</p>
        <p><b style="color: #ff6570; font-weight: 900;">TOP LEFT (%):</b> The percentage of top jackpots unclaimed. If this hits <b style="color: #ffffff;">0%</b>, avoid the card—all top prizes have already been cashed in.</p>
    </div>
    """, unsafe_allow_html=True)

if df.empty:
    st.warning("No summary data found. Run `python3 lottery_scraper.py` first to generate `scratch_games_summary.csv`.")
    st.stop()

# --- Quick Filter Controls ---
col_filter1, col_filter2 = st.columns([1, 1])

with col_filter1:
    hide_retired = st.checkbox("Hide Retired Games", value=True)

prices = ["All"] + sorted(list(df["ticket_price"].unique()))
with col_filter2:
    selected_price = st.selectbox("Ticket Price Filter", prices)

sort_choice = st.selectbox(
    "Sort Strategy",
    [
        "Best Expected Value (EV)",
        "Most Top Prizes Left (%)",
        "Most Tickets Sold (%)",
        "Ticket Price (High to Low)"
    ]
)

# Apply filters
filtered_df = df.copy()
if hide_retired:
    filtered_df = filtered_df[filtered_df["status"] == "ACTIVE"]

if selected_price != "All":
    filtered_df = filtered_df[filtered_df["ticket_price"] == int(selected_price)]

# Apply sorting
if sort_choice == "Best Expected Value (EV)":
    filtered_df = filtered_df.sort_values(by="expected_value", ascending=False)
elif sort_choice == "Most Top Prizes Left (%)":
    filtered_df = filtered_df.sort_values(by="top_prize_percent_remaining", ascending=False)
elif sort_choice == "Most Tickets Sold (%)":
    filtered_df = filtered_df.sort_values(by="percent_sold", ascending=False)
elif sort_choice == "Ticket Price (High to Low)":
    filtered_df = filtered_df.sort_values(by="ticket_price", ascending=False)

st.markdown(f"<p style='color: #65fff4; font-size: 1.05rem; font-weight: 900; margin-top: 14px; letter-spacing: 0.5px;'>SHOWING {len(filtered_df)} GAMES IN CIRCULATION</p>", unsafe_allow_html=True)

# --- Card Feed ---
for _, game in filtered_df.iterrows():
    is_active = game["status"] == "ACTIVE"
    status_dot = "🟢" if is_active else "🔴"
    
    with st.container():
        # Title Bar with Large Pink Price Badge
        st.markdown(f"""
        <div class="game-card-header">
            <span class="game-title-text">{status_dot} {game['game_name']}</span>
            <span class="ticket-badge">${game['ticket_price']}</span>
        </div>
        """, unsafe_allow_html=True)

        # 3 Framed Metric Tiles (Padded, Bordered & Side-by-Side)
        st.markdown(f"""
        <div class="metric-tiles-row">
            <div class="metric-tile">
                <div class="metric-tile-label">EV (VAL)</div>
                <div class="metric-tile-val">${game['expected_value']:.2f}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-tile-label">TOP CLAIM</div>
                <div class="metric-tile-val">{int(game['top_prizes_remaining'])}/{int(game['top_prizes_total'])}</div>
            </div>
            <div class="metric-tile">
                <div class="metric-tile-label">TOP LEFT</div>
                <div class="metric-tile-val">{game['top_prize_percent_remaining']:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Detailed Breakdown Expander
        with st.expander(f"🔍 DEEP DIVE: #{game['game_id']} {game['game_name']}"):
            st.markdown(f"<p style='margin: 0; color: #94a3b8; font-weight: 800; font-size: 1.05rem;'>Top Jackpot Amount: <b style='color: #ffffff; font-size: 1.25rem; font-weight: 900;'>{game['top_prize_amount']}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0; color: #94a3b8; font-weight: 800; font-size: 1.05rem;'>Overall Odds: <b style='color: #ffffff; font-weight: 900;'>1 in {game['overall_odds']}</b></p>", unsafe_allow_html=True)
            
            # Sales Progress Bar
            sold_pct = min(max(game["percent_sold"], 0.0), 100.0)
            st.markdown(f"<p style='margin-top: 14px; margin-bottom: 4px; font-weight: 900; color: #65fff4; font-size: 1.05rem;'>Print Run Depletion: <span style='color: #65ffa7;'>{sold_pct:.1f}% Sold</span></p>", unsafe_allow_html=True)
            st.progress(sold_pct / 100.0)

            # Raw Pool Estimates
            sub1, sub2 = st.columns(2)
            sub1.markdown(f"<p style='color: #94a3b8; font-size: 0.95rem; font-weight: 800;'>Original Pool:<br><b style='color: #ffffff; font-size: 1.15rem; font-weight: 900;'>{int(game['est_tickets_total']):,} tickets</b></p>", unsafe_allow_html=True)
            sub2.markdown(f"<p style='color: #94a3b8; font-size: 0.95rem; font-weight: 800;'>Tickets Remaining:<br><b style='color: #ffffff; font-size: 1.15rem; font-weight: 900;'>{int(game['est_tickets_remaining']):,} tickets</b></p>", unsafe_allow_html=True)

            # Alerts
            if game['top_prizes_remaining'] == 0 and is_active:
                st.markdown("""
                <div class="avoid-alert">
                    ⚠️ <b>DEAD JACKPOT:</b> All top grand prizes have already been cashed in. There are zero jackpots left in this print run.
                </div>
                """, unsafe_allow_html=True)
            elif game['percent_sold'] >= 65.0 and game['top_prize_percent_remaining'] >= 50.0:
                st.markdown("""
                <div class="edge-alert">
                    🔥 <b>HIGH EDGE:</b> Over 65% of all tickets are gone, but at least half of the top jackpots remain unclaimed!
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"<p style='color: #64748b; font-size: 0.9rem; font-weight: 800; margin-top: 14px;'>Status: <b>{game['status']}</b> | Last Synced: {game['last_updated']}</p>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)