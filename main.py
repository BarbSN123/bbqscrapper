import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import time

# ========== CONFIG ==========
url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

branches_config = {
    "14": {
        "name": "Koramangala",
        "slots": {
            "12:00:00": 1105  # ✅ only one slot for testing
        },
    }
}


def fetch_slots(start_date, days=1):
    all_slots = []
    progress = st.progress(0, text="Fetching buffet data...")

    for branch_idx, (branch_id, branch_info) in enumerate(branches_config.items(), start=1):
        branch_name = branch_info["name"]
        slot_map = branch_info.get("slots", {})

        for d in range(days):
            date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")

            for i, (time_str, slot_id) in enumerate(slot_map.items(), start=1):
                progress.progress(
                    min((branch_idx / len(branches_config)), 1.0),
                    text=f"Fetching {branch_name} - {time_str} ({date_str})..."
                )

                payload = {
                    "branch_id": branch_id,
                    "reservation_date": date_str,
                    "reservation_time": time_str,
                    "slot_id": slot_id
                }

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
                        all_slots.append({
                            "Branch": branch_name,
                            "Branch ID": branch_id,
                            "Date": date_str,
                            "Slot Time": time_str,
                            "Error": "No buffet data"
                        })
                        continue

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

                except requests.exceptions.Timeout:
                    st.error(f"⚠️ Timeout for {branch_name} ({branch_id}) - {date_str} {time_str}")
                except Exception as e:
                    st.error(f"❌ Error fetching {branch_name} ({branch_id}) - {date_str} {time_str}: {e}")

                time.sleep(0.2)

    progress.empty()
    return pd.DataFrame(all_slots)


# ========== STREAMLIT DASHBOARD ==========
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
st.title("🍽️ Barbeque Nation Buffet Monitor")

# Sidebar Controls
st.sidebar.header("⚙️ Controls")
interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=36000, value=36000, step=30)
days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, value=1)

branch_names = ["All Branches"] + [info["name"] for info in branches_config.values()]
selected_branch = st.sidebar.selectbox("Select Branch", branch_names)

# ========== AUTOREFRESH ==========
st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# ========== MAIN DATA FETCH ==========
df = fetch_slots(datetime.today(), days=days_to_fetch)
if selected_branch != "All Branches":
    df = df[df["Branch"] == selected_branch]

# ========== DISPLAY ==========
st.subheader(f"📅 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
st.dataframe(df, use_container_width=True)
st.write("Total Rows:", len(df))
