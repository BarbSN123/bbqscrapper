import requests
import pandas as pd
import streamlit as st
import time
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# ===================== CONFIG =====================
url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

branches_config = {
    "14": {
        "name": "Koramangala",
        "slots": {
            "12:00:00": 1105, "12:30:00": 1105, "13:00:00": 1105,
            "13:30:00": 1105, "14:00:00": 1105, "14:30:00": 1106,
            "15:00:00": 1106, "15:30:00": 1106, "16:00:00": 1106,
            "16:30:00": 1106, "17:00:00": 1106, "17:30:00": 1106,
            "18:00:00": 1106, "18:30:00": 1107, "19:00:00": 1107,
            "19:30:00": 1107, "20:00:00": 1107, "20:30:00": 1107,
            "21:00:00": 1108, "21:30:00": 1108, "22:00:00": 1108,
            "22:30:00": 1108
        }
    },
    "133": {
        "name": "Rukmani Colony AS Rao Nagar Hyderabad",
        "slots": {
            "12:00:00": 740, "12:30:00": 740, "13:00:00": 740,
            "13:30:00": 740, "14:00:00": 740, "14:30:00": 741,
            "15:00:00": 741, "15:30:00": 741, "16:00:00": 741,
            "16:30:00": 741, "17:00:00": 741, "17:30:00": 741,
            "18:00:00": 741, "18:30:00": 742, "19:00:00": 742,
            "19:30:00": 742, "20:00:00": 742, "20:30:00": 742,
            "21:00:00": 743, "21:30:00": 743, "22:00:00": 743,
            "22:30:00": 743
        }
    }
}

# Detect if running in Streamlit Cloud or similar
IS_DEPLOYED = any(
    k in os.environ for k in [
        "STREAMLIT_SERVER", "RENDER", "RAILWAY_ENVIRONMENT", "VERCEL"
    ]
)

# ===================== FETCH FUNCTION =====================
def fetch_slots(start_date, days=1):
    all_slots = []
    failed_slots = []
    total_requests = 0

    progress = st.progress(0, text="Fetching buffet data...")

    for branch_idx, (branch_id, branch_info) in enumerate(branches_config.items(), start=1):
        branch_name = branch_info["name"]
        slot_map = branch_info.get("slots", {})

        # Limit slots when deployed
        slot_items = list(slot_map.items())
        if IS_DEPLOYED:
            slot_items = slot_items[:3]  # Fetch only 3 slots per branch online

        for d in range(days):
            date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")

            for i, (time_str, slot_id) in enumerate(slot_items, start=1):
                total_requests += 1
                progress.progress(
                    min((branch_idx / len(branches_config)), 1.0),
                    text=f"Fetching {branch_name} - {time_str} ({date_str})..."
                )

                payload = {
                    "branch_id": str(branch_id),
                    "reservation_date": date_str,
                    "reservation_time": time_str,
                    "slot_id": slot_id
                }

                success = False
                last_error = None
                for attempt in range(3):
                    try:
                        r = requests.post(url, json=payload, headers=headers, timeout=10)
                        r.raise_for_status()
                        data = r.json()

                        buffets = (
                            data.get("results", {})
                                .get("buffets", {})
                                .get("buffet_data", [])
                                or []
                        )

                        if not buffets:
                            failed_slots.append(
                                f"⚠️ No data for {branch_name} - {date_str} {time_str}"
                            )
                            break

                        for b in buffets:
                            all_slots.append({
                                "Branch": branch_name,
                                "Branch ID": branch_id,
                                "Date": date_str,
                                "Slot Time": time_str,
                                "Period": b.get("period", {}).get("periodName", ""),
                                "Customer Type": b.get("customerType", ""),
                                "Food Type": b.get("foodType", ""),
                                "Plan": b.get("displayName", ""),
                                "Price": b.get("totalAmount", ""),
                                "Original Price": b.get("originalPrice", "")
                            })

                        success = True
                        break

                    except requests.exceptions.RequestException as e:
                        last_error = f"HTTP error: {e}"
                        time.sleep(1)
                    except Exception as e:
                        last_error = f"Unexpected: {e}"
                        break

                if not success:
                    failed_slots.append(
                        f"❌ Failed after 3 retries for {branch_name} - {date_str} {time_str} | {last_error}"
                    )

                time.sleep(0.2)

    progress.empty()

    if failed_slots:
        st.warning("Some slots failed to fetch:")
        for msg in failed_slots:
            st.write(msg)

    return pd.DataFrame(all_slots)

# ===================== STREAMLIT DASHBOARD =====================
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
st.title("🍽️ Barbeque Nation Buffet Monitor")

if IS_DEPLOYED:
    st.info("Running in deployed mode — limiting API calls per branch to 3 to prevent timeouts. ⚡")

# Sidebar Controls
st.sidebar.header("⚙️ Controls")
interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=30, value=60, step=30)
days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, value=1)
branch_names = ["All Branches"] + [info["name"] for info in branches_config.values()]
selected_branch = st.sidebar.selectbox("Select Branch", branch_names)

# Auto-refresh
count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# Session State
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

# Fetch main data
df = fetch_slots(datetime.today(), days=days_to_fetch)
if selected_branch != "All Branches":
    df = df[df["Branch"] == selected_branch]

# Detect changes
changes_detected = False
if not st.session_state.first_run and not st.session_state.prev_data.empty:
    common_cols = [c for c in st.session_state.prev_data.columns if c in df.columns]
    df_cmp = df[common_cols].reset_index(drop=True)
    prev_cmp = st.session_state.prev_data[common_cols].reset_index(drop=True)
    difference = df_cmp[df_cmp.ne(prev_cmp).any(axis=1)]
    if not difference.empty:
        st.session_state.last_changes = difference
        changes_detected = True
    else:
        st.session_state.last_changes = pd.DataFrame()
else:
    st.session_state.last_changes = pd.DataFrame()

st.session_state.prev_data = df.copy()
st.session_state.last_updated = datetime.now().strftime("%H:%M:%S")
st.session_state.first_run = False

# Update sidebar log
log_entry = f"{st.session_state.last_updated} — {'✅ Changes detected' if changes_detected else 'No change'}"
st.session_state.log.insert(0, log_entry)
if len(st.session_state.log) > 10:
    st.session_state.log = st.session_state.log[:10]

st.sidebar.markdown("### 🕓 Refresh Log")
for entry in st.session_state.log:
    st.sidebar.write(entry)

# Display data
st.subheader(f"📅 Last Updated: {st.session_state.last_updated}")

if not st.session_state.last_changes.empty:
    st.markdown("### 🔄 Recently Changed Data")
    st.dataframe(st.session_state.last_changes, use_container_width=True)
    st.markdown("---")

st.markdown("### 📊 Current Buffet Data")
if df.empty:
    st.error("No buffet data found. Please check API or slot configuration.")
else:
    st.dataframe(df, use_container_width=True)
    st.write("Total Rows:", len(df))
