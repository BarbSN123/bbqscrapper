import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import time
import requests


# ========= CONFIG =========
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")

# Your live GitHub JSON link
# GITHUB_JSON_URL = "https://raw.githubusercontent.com/diyanshu-anand/bbq-data/main/json/buffet_data.json"  Cache issues
GITHUB_JSON_URL = f"https://raw.githubusercontent.com/diyanshu-anand/bbq-data/main/json/buffet_data.json?nocache={int(time.time())}"
# response = requests.get(url, headers={"Cache-Control": "no-cache"})
# data = response.json()

st.title("🍽️ Barbeque Nation Buffet Monitor (GitHub Synced)")

# ========= SIDEBAR =========
st.sidebar.header("⚙️ Controls")
interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=60, value=3600, step=30)

# ========= AUTO REFRESH =========
count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# ========= SESSION STATE =========
if "prev_data" not in st.session_state:
    st.session_state.prev_data = pd.DataFrame()
if "last_changes" not in st.session_state:
    st.session_state.last_changes = pd.DataFrame()
if "last_updated" not in st.session_state:
    st.session_state.last_updated = None
if "first_run" not in st.session_state:
    st.session_state.first_run = True
if "log" not in st.session_state:
    st.session_state.log = []

# ========= FETCH DATA =========
@st.cache_data(ttl=120)
def fetch_from_github():
    try:
        res = requests.get(GITHUB_JSON_URL)
        res.raise_for_status()
        raw = res.json()

        # Handle both old and new formats
        if isinstance(raw, dict) and "records" in raw:
            df = pd.DataFrame(raw["records"])
            gen_time = raw.get("generated_at", "Unknown")
        else:
            df = pd.DataFrame(raw)
            gen_time = "Unknown"

        # Convert date column to datetime for filtering
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        return df, gen_time
    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
        return pd.DataFrame(), None


df, generated_at = fetch_from_github()

if df.empty:
    st.warning("No buffet data found in GitHub file.")
    st.stop()

# ========= DATE FILTER =========
min_date = df["Date"].min()
max_date = df["Date"].max()

if pd.isna(min_date) or pd.isna(max_date):
    min_date = datetime.now().date()
    max_date = datetime.now().date() + timedelta(days=30)

selected_date = st.sidebar.date_input(
    "Select Date", 
    value=datetime.now().date(), 
    min_value=min_date.date(), 
    max_value=max_date.date()
)

# Filter by selected date
df = df[df["Date"].dt.date == selected_date]

# ========= BRANCH FILTER =========
branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())
selected_branch = st.sidebar.selectbox("Select Branch", branches)

if selected_branch != "All Branches":
    df = df[df["Branch"] == selected_branch]

# ========= CHANGE DETECTION =========
changes_detected = False
if not st.session_state.first_run and not st.session_state.prev_data.empty:
    common_cols = [c for c in st.session_state.prev_data.columns if c in df.columns]
    new_data = df[common_cols].reset_index(drop=True)
    old_data = st.session_state.prev_data[common_cols].reset_index(drop=True)

    diff = new_data[new_data.ne(old_data).any(axis=1)]
    if not diff.empty:
        st.session_state.last_changes = diff
        changes_detected = True
    else:
        st.session_state.last_changes = pd.DataFrame()
else:
    st.session_state.last_changes = pd.DataFrame()

# ========= UPDATE SESSION STATE =========
st.session_state.prev_data = df.copy()
st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.session_state.first_run = False

# ========= UPDATE LOG =========
log_entry = f"{st.session_state.last_updated} — {'✅ Changes detected' if changes_detected else 'No change'}"
st.session_state.log.insert(0, log_entry)
if len(st.session_state.log) > 10:
    st.session_state.log = st.session_state.log[:10]

# ========= SIDEBAR LOG =========
st.sidebar.markdown("### 🕓 Refresh Log")
for entry in st.session_state.log:
    st.sidebar.write(entry)

# ========= DISPLAY =========
st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")
st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

if not st.session_state.last_changes.empty:
    st.markdown("### 🔄 Recently Changed Data")
    st.dataframe(st.session_state.last_changes, use_container_width=True)
    st.markdown("---")

if df.empty:
    st.warning("No data found for the selected date and branch.")
else:
    st.markdown("### 📊 Current Buffet Data")
    st.dataframe(df, use_container_width=True)
    st.write("Total Rows:", len(df))
