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

# ========== LICENSE / SELF-DESTRUCT CONFIG ==========
# Set expiry date (3 months from now)
expiry_date = datetime(2026, 1, 10)  # Taking 3 months from release
correct_password = "NIKHILbhaiya10102052" # Password to stop self destructor 

# Initialize session state for password input
if "license_unlocked" not in st.session_state:
    st.session_state.license_unlocked = False

# Check if expired
if datetime.today() > expiry_date and not st.session_state.license_unlocked:
    st.warning("⚠️ This program has expired. Please enter your password to continue.")
    
    password_input = st.text_input("Enter password to unlock:", type="password")
    
    if password_input:
        if password_input == correct_password:
            st.session_state.license_unlocked = True
            st.success("✅ Password accepted. You can now use the program.")
        else:
            st.error("❌ Incorrect password. Program will not run.")
    
    # Stop running the app until password is correct or expiry is not reached
    st.stop()

# ========== CONFIG ==========
url = "https://www.barbequenation.com/api/v1/menu-buffet-price"
headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

branch_config = {
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

# ========== BRANCH CONFIG DETAILS ==========
branches_config = {
    "171": {   # Branch ID as string Thiis is not edited has to be done at last
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
    "133": {   # Another branch
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
    },
    "25":{
        "name":"Banajara Hills, Hyderabad",
        "slots": {
            "12:00:00": 97, "12:30:00": 97, "13:00:00": 97,
            "13:30:00": 97, "14:00:00": 97, "14:30:00": 98,
            "15:00:00": 98, "15:30:00": 98, "16:00:00": 98,
            "16:30:00": 98, "17:00:00": 98, "17:30:00": 98,
            "18:00:00": 98, "18:30:00": 99, "19:00:00": 99,
            "19:30:00": 99, "20:00:00": 99, "20:30:00": 99,
            "21:00:00": 100, "21:30:00": 100, "22:00:00": 100,
            "22:30:00": 100
        }
    },
    "646":{
        "name":"Phoenix Centaurus, Gachibowli",
        "slots": {
            "12:00:00": 2176, "12:30:00": 2176, "13:00:00": 2176,
            "13:30:00": 2176, "14:00:00": 2176, "14:30:00": 2177,
            "15:00:00": 2177, "15:30:00": 2177, "16:00:00": 2177,
            "16:30:00": 2177, "17:00:00": 2177, "17:30:00": 2177,
            "18:00:00": 2177, "18:30:00": 2178, "19:00:00": 2178,
            "19:30:00": 2178, "20:00:00": 2178, "20:30:00": 2178,
            "21:00:00": 2180, "21:30:00": 2180, "22:00:00": 2180,
            "22:30:00": 2180
        }
    },
    "117":{
        "name":"Alcazar Mall, Jubilee Hills",
        "slots":{
            "12:00:00": 509, "12:30:00": 509, "13:00:00": 509,
            "13:30:00": 509, "14:00:00": 509, "14:30:00": 510,
            "15:00:00": 510, "15:30:00": 510, "16:00:00": 510,
            "16:30:00": 510, "17:00:00": 510, "17:30:00": 510,
            "18:00:00": 510, "18:30:00": 511, "19:00:00": 511,
            "19:30:00": 511, "20:00:00": 511, "20:30:00": 511,
            "21:00:00": 512, "21:30:00": 512, "22:00:00": 512,
            "22:30:00": 512
        }
    },
    "228": {
        "name":" Kompally, Hyderrabad",
        "slots": {
            "12:00:00": 1667, "12:30:00": 1667, "13:00:00": 1667,
            "13:30:00": 1667, "14:00:00": 1667, "14:30:00": 1668,
            "15:00:00": 1668, "15:30:00": 1668, "16:00:00": 1668,
            "16:30:00": 1668, "17:00:00": 1668, "17:30:00": 1668,
            "18:00:00": 1668, "18:30:00": 1669, "19:00:00": 1669,
            "19:30:00": 1669, "20:00:00": 1669, "20:30:00": 1669,
            "21:00:00": 1670, "21:30:00": 1670, "22:00:00": 1670,
            "22:30:00": 1670
        }
    },
    "557":{
        "name":"DSL Virtue Mall, Uppal",
        "slots": {
            "12:00:00": 1904, "12:30:00": 1904, "13:00:00": 1904,
            "13:30:00": 1904, "14:00:00": 1904, "14:30:00": 1905,
            "15:00:00": 1905, "15:30:00": 1905, "16:00:00": 1905,
            "16:30:00": 1905, "17:00:00": 1905, "17:30:00": 1905,
            "18:00:00": 1905, "18:30:00": 1906, "19:00:00": 1906,
            "19:30:00": 1906, "20:00:00": 1906, "20:30:00": 1906,
            "21:00:00": 1907, "21:30:00": 1907, "22:00:00": 1907,
            "22:30:00": 1907
        }
    },
    "214":{
        "name":"GSM Mall Miyapur",
        "slots":{
            "12:00:00": 1630, "12:30:00": 1630, "13:00:00": 1630,
            "13:30:00": 1630, "14:00:00": 1630, "14:30:00": 1631,
            "15:00:00": 1631, "15:30:00": 1631, "16:00:00": 1631,
            "16:30:00": 2020, "17:00:00": 2020, "17:30:00": 1632,
            "18:00:00": 1632, "18:30:00": 1632, "19:00:00": 1632,
            "19:30:00": 1632, "20:00:00": 1632, "20:30:00": 1632,
            "21:00:00": 1633, "21:30:00": 1633, "22:00:00": 1633,
            "22:30:00": 1633
        }
    },
    "233":{
        "name":"City Plaza Building, Abids",
        "slots":{
            "12:00:00": 1687, "12:30:00": 1687, "13:00:00": 1687,
            "13:30:00": 1687, "14:00:00": 1687, "14:30:00": 1688,
            "15:00:00": 1688, "15:30:00": 1688, "16:00:00": 1688,
            "16:30:00": 1688, "17:00:00": 1688, "17:30:00": 1688,
            "18:00:00": 1688, "18:30:00": 1689, "19:00:00": 1689,
            "19:30:00": 1689, "20:00:00": 1689, "20:30:00": 1689,
            "21:00:00": 1690, "21:30:00": 1690, "22:00:00": 1690,
            "22:30:00": 1690
        }
    },
    "149":{
        "name":"Kothapet",
        "slots":{
            "12:00:00": 837, "12:30:00": 837, "13:00:00": 837,
            "13:30:00": 837, "14:00:00": 837, "14:30:00": 838,
            "15:00:00": 838, "15:30:00": 838, "16:00:00": 838,
            "16:30:00": 838, "17:00:00": 838, "17:30:00": 838,
            "18:00:00": 838, "18:30:00": 839, "19:00:00": 839,
            "19:30:00": 839, "20:00:00": 839, "20:30:00": 839,
            "21:00:00": 840, "21:30:00": 840, "22:00:00": 840,
            "22:30:00": 840
        }
    },
    "60":{
        "name":"Centro Mall, MG Road",
        "slots":{
            "12:00:00": 235, "12:30:00": 235, "13:00:00": 235,
            "13:30:00": 235, "14:00:00": 235, "14:30:00": 236,
            "15:00:00": 236, "15:30:00": 236, "16:00:00": 2171,
            "16:30:00": 2171, "17:00:00": 2171, "17:30:00": 2171,
            "18:00:00": 2171, "18:30:00": 237, "19:00:00": 237,
            "19:30:00": 237, "20:00:00": 237, "20:30:00": 237,
            "21:00:00": 238, "21:30:00": 238, "22:00:00": 238,
            "22:30:00": 238
        }
    },
    "225":{
        "name":"Madhurawada",
        "slots":{
            "12:00:00": 1658, "12:30:00": 1658, "13:00:00": 1658,
            "13:30:00": 1658, "14:00:00": 1658, "14:30:00": 1659,
            "15:00:00": 1659, "15:30:00": 1659, "16:00:00": 1659,
            "16:30:00": 1659, "17:00:00": 1659, "17:30:00": 1659,
            "18:00:00": 1659, "18:30:00": 1660, "19:00:00": 1660,
            "19:30:00": 1660, "20:00:00": 1660, "20:30:00": 1660,
            "21:00:00": 1661, "21:30:00": 1661, "22:00:00": 1661,
            "22:30:00": 1661
        }
    },
    "15":{
        "name":"JP Nagar",
        "slots":{
            "12:00:00": 57, "12:30:00": 57, "13:00:00": 57,
            "13:30:00": 57, "14:00:00": 57, "14:30:00": 58,
            "15:00:00": 58, "15:30:00": 58, "16:00:00": 58,
            "16:30:00": 58, "17:00:00": 58, "17:30:00": 58,
            "18:00:00": 58, "18:30:00": 59, "19:00:00": 59,
            "19:30:00": 59, "20:00:00": 59, "20:30:00": 59,
            "21:00:00": 60, "21:30:00": 60, "22:00:00": 60,
            "22:30:00": 60
        }
    },
    "17":{
        "name":"Electronic City- Ph I",
        "slots":{
            "12:00:00": 65, "12:30:00": 65, "13:00:00": 65,
            "13:30:00": 65, "14:00:00": 65, "14:30:00": 66,
            "15:00:00": 66, "15:30:00": 66, "16:00:00": 66,
            "16:30:00": 66, "17:00:00": 66, "17:30:00": 66,
            "18:00:00": 66, "18:30:00": 67, "19:00:00": 67,
            "19:30:00": 67, "20:00:00": 67, "20:30:00": 67,
            "21:00:00": 68, "21:30:00": 68, "22:00:00": 68,
            "22:30:00": 68
        }
    },
    "19":{
        "name":"Kalyan Nagar",
        "slots":{
            "12:00:00": 69, "12:30:00": 69, "13:00:00": 69,
            "13:30:00": 69, "14:00:00": 69, "14:30:00": 70,
            "15:00:00": 70, "15:30:00": 70, "16:00:00": 70,
            "16:30:00": 70, "17:00:00": 70, "17:30:00": 70,
            "18:00:00": 70, "18:30:00": 71, "19:00:00": 71,
            "19:30:00": 71, "20:00:00": 71, "20:30:00": 71,
            "21:00:00": 72, "21:30:00": 72, "22:00:00": 72,
            "22:30:00": 72
        }
    },
    "14":{
        "name":"Koramangala 1st Block",
        "slots":{
            "12:00:00": 53, "12:30:00": 53, "13:00:00": 53,
            "13:30:00": 53, "14:00:00": 53, "14:30:00": 54,
            "15:00:00": 54, "15:30:00": 54, "16:00:00": 54,
            "16:30:00": 54, "17:00:00": 54, "17:30:00": 54,
            "18:00:00": 54, "18:30:00": 55, "19:00:00": 55,
            "19:30:00": 55, "20:00:00": 55, "20:30:00": 55,
            "21:00:00": 56, "21:30:00": 56, "22:00:00": 56,
            "22:30:00": 56
        }
    },
    "545":{
        "name":"More Mega Mall, Marathahalli",
        "slots":{
            "12:00:00": 1898, "12:30:00": 1898, "13:00:00": 1898,
            "13:30:00": 1898, "14:00:00": 1898, "14:30:00": 1899,
            "15:00:00": 1899, "15:30:00": 1899, "16:00:00": 1899,
            "16:30:00": 1899, "17:00:00": 1899, "17:30:00": 1899,
            "18:00:00": 1899, "18:30:00": 1900, "19:00:00": 1900,
            "19:30:00": 1900, "20:00:00": 1900, "20:30:00": 1900,
            "21:00:00": 1901, "21:30:00": 1901, "22:00:00": 1901,
            "22:30:00": 1901
        }
    },
    "301":{
        "name":"NEXUS SANTHINIKETHAN ,WHITEFIELD",
        "slots":{
            "12:00:00": 1753, "12:30:00": 1753, "13:00:00": 1753,
            "13:30:00": 1753, "14:00:00": 1753, "14:30:00": 1754,
            "15:00:00": 1754, "15:30:00": 1754, "16:00:00": 1754,
            "16:30:00": 1754, "17:00:00": 1754, "17:30:00": 1754,
            "18:00:00": 1754, "18:30:00": 1756, "19:00:00": 1756,
            "19:30:00": 1756, "20:00:00": 1756, "20:30:00": 1756,
            "21:00:00": 1757, "21:30:00": 1757, "22:00:00": 1757,
            "22:30:00": 1757
        }
    },
    "94":{
        "name":"Yelahanka",
        "slots":{
            "12:00:00": 371, "12:30:00": 371, "13:00:00": 371,
            "13:30:00": 371, "14:00:00": 371, "14:30:00": 372,
            "15:00:00": 372, "15:30:00": 372, "16:00:00": 372,
            "16:30:00": 372, "17:00:00": 372, "17:30:00": 372,
            "18:00:00": 372, "18:30:00": 373, "19:00:00": 373,
            "19:30:00": 373, "20:00:00": 373, "20:30:00": 373,
            "21:00:00": 374, "21:30:00": 374, "22:00:00": 374,
            "22:30:00": 374
        }
    },
    "487":{
        "name":"Lulu Global Mall, Rajajinagar",
        "slots":{
            "12:00:00": 1790, "12:30:00": 1790, "13:00:00": 1790,
            "13:30:00": 1790, "14:00:00": 1790, "14:30:00": 1791,
            "15:00:00": 1791, "15:30:00": 1791, "16:00:00": 1791,
            "16:30:00": 1791, "17:00:00": 1791, "17:30:00": 1791,
            "18:00:00": 1791, "18:30:00": 1792, "19:00:00": 1792,
            "19:30:00": 1792, "20:00:00": 1792, "20:30:00": 1792,
            "21:00:00": 1793, "21:30:00": 1793, "22:00:00": 1793,
            "22:30:00": 1793
        }
    },
    "11":{
        "name":"Vadapalani",
        "slots":{
            "12:00:00": 41, "12:30:00": 41, "13:00:00": 41,
            "13:30:00": 41, "14:00:00": 41, "14:30:00": 42,
            "15:00:00": 42, "15:30:00": 42, "16:00:00": 42,
            "16:30:00": 42, "17:00:00": 42, "17:30:00": 42,
            "18:00:00": 42, "18:30:00": 43, "19:00:00": 43,
            "19:30:00": 43, "20:00:00": 43, "20:30:00": 43,
            "21:00:00": 44, "21:30:00": 44, "22:00:00": 44,
            "22:30:00": 44
        }
    },
    "119":{
        "name":"Chromepet",
        "slots":{
            "12:00:00": 517, "12:30:00": 517, "13:00:00": 517,
            "13:30:00": 517, "14:00:00": 517, "14:30:00": 518,
            "15:00:00": 518, "15:30:00": 518, "16:00:00": 518,
            "16:30:00": 518, "17:00:00": 518, "17:30:00": 518,
            "18:00:00": 518, "18:30:00": 519, "19:00:00": 519,
            "19:30:00": 519, "20:00:00": 519, "20:30:00": 519,
            "21:00:00": 520, "21:30:00": 520, "22:00:00": 520,
            "22:30:00": 520
        }
    },
    "63":{
        "name":"Town Hall, Coimbatore",
        "slots":{
            "12:00:00": 247, "12:30:00": 247, "13:00:00": 247,
            "13:30:00": 247, "14:00:00": 247, "14:30:00": 248,
            "15:00:00": 248, "15:30:00": 248, "16:00:00": 248,
            "16:30:00": 248, "17:00:00": 248, "17:30:00": 248,
            "18:00:00": 248, "18:30:00": 249, "19:00:00": 249,
            "19:30:00": 249, "20:00:00": 249, "20:30:00": 249,
            "21:00:00": 250, "21:30:00": 250, "22:00:00": 250,
            "22:30:00": 250
        }
    },
    "10":{
        "name":"T Nagar Bazullah Road",
        "slots":{
            "12:00:00": 37, "12:30:00": 37, "13:00:00": 37,
            "13:30:00": 37, "14:00:00": 37, "14:30:00": 38,
            "15:00:00": 38, "15:30:00": 38, "16:00:00": 38,
            "16:30:00": 38, "17:00:00": 38, "17:30:00": 38,
            "18:00:00": 38, "18:30:00": 39, "19:00:00": 39,
            "19:30:00": 39, "20:00:00": 39, "20:30:00": 39,
            "21:00:00": 40, "21:30:00": 40, "22:00:00": 40,
            "22:30:00": 40
        }
    },
    "127":{
        "name":"DLF Porur",
        "slots":{
            "12:00:00": 549, "12:30:00": 549, "13:00:00": 549,
            "13:30:00": 549, "14:00:00": 549, "14:30:00": 550,
            "15:00:00": 550, "15:30:00": 550, "16:00:00": 550,
            "16:30:00": 550, "17:00:00": 550, "17:30:00": 550,
            "18:00:00": 550, "18:30:00": 551, "19:00:00": 551,
            "19:30:00": 551, "20:00:00": 551, "20:30:00": 551,
            "21:00:00": 552, "21:30:00": 552, "22:00:00": 552,
            "22:30:00": 552
        }
    },
    "28":{
        "name":"The Grand Mall Velachery",
        "slots":{
            "12:00:00": 110, "12:30:00": 110, "13:00:00": 110,
            "13:30:00": 110, "14:00:00": 110, "14:30:00": 111,
            "15:00:00": 111, "15:30:00": 111, "16:00:00": 111,
            "16:30:00": 112, "17:00:00": 112, "17:30:00": 112,
            "18:00:00": 112, "18:30:00": 112, "19:00:00": 112,
            "19:30:00": 112, "20:00:00": 112, "20:30:00": 112,
            "21:00:00": 113, "21:30:00": 113, "22:00:00": 113,
            "22:30:00": 113
        }
    },
    "8":{
        "name":"Omr",
        "slots":{
            "12:00:00": 29, "12:30:00": 29, "13:00:00": 29,
            "13:30:00": 29, "14:00:00": 29, "14:30:00": 30,
            "15:00:00": 30, "15:30:00": 30, "16:00:00": 31,
            "16:30:00": 31, "17:00:00": 31, "17:30:00": 31,
            "18:00:00": 31, "18:30:00": 31, "19:00:00": 31,
            "19:30:00": 31, "20:00:00": 31, "20:30:00": 31,
            "21:00:00": 32, "21:30:00": 32, "22:00:00": 32,
            "22:30:00": 32
        }
    },
    "75":{
        "name":"Sachivalaya Marg",
        "slots":{
            "12:00:00": 299, "12:30:00": 299, "13:00:00": 299,
            "13:30:00": 299, "14:00:00": 299, "14:30:00": 300,
            "15:00:00": 300, "15:30:00": 300, "16:00:00": 310,
            "16:30:00": 310, "17:00:00": 310, "17:30:00": 310,
            "18:00:00": 310, "18:30:00": 301, "19:00:00": 301,
            "19:30:00": 301, "20:00:00": 301, "20:30:00": 301,
            "21:00:00": 302, "21:30:00": 302, "22:00:00": 302,
            "22:30:00": 302
        }
    },
    "295":{
        "name":"Udeshna Building",
        "slots":{
            "12:00:00": 1707, "12:30:00": 1707, "13:00:00": 1707,
            "13:30:00": 1707, "14:00:00": 1707, "14:30:00": 1708,
            "15:00:00": 1708, "15:30:00": 1708, "16:00:00": 1708,
            "16:30:00": 1708, "17:00:00": 1708, "17:30:00": 1708,
            "18:00:00": 1708, "18:30:00": 1709, "19:00:00": 1709,
            "19:30:00": 1709, "20:00:00": 1709, "20:30:00": 1709,
            "21:00:00": 1710, "21:30:00": 1710, "22:00:00": 1710,
            "22:30:00": 1710
        }
    },
    "101":{
        "name":"One Mall, Fraser Road Area",
        "slots":{
            "12:00:00": 451, "12:30:00": 451, "13:00:00": 451,
            "13:30:00": 451, "14:00:00": 451, "14:30:00": 452,
            "15:00:00": 452, "15:30:00": 452, "16:00:00": 452,
            "16:30:00": 452, "17:00:00": 452, "17:30:00": 452,
            "18:00:00": 452, "18:30:00": 453, "19:00:00": 453,
            "19:30:00": 453, "20:00:00": 453, "20:30:00": 453,
            "21:00:00": 1103, "21:30:00": 1103, "22:00:00": 1103,
            "22:30:00": 1103
        }
    },
    "501":{
        "name":"Platina Mall, Howrah",
        "slots":{
            "12:00:00": 1882, "12:30:00": 1882, "13:00:00": 1882,
            "13:30:00": 1882, "14:00:00": 1882, "14:30:00": 1883,
            "15:00:00": 1883, "15:30:00": 1883, "16:00:00": 1883,
            "16:30:00": 1883, "17:00:00": 1883, "17:30:00": 1883,
            "18:00:00": 1883, "18:30:00": 1884, "19:00:00": 1884,
            "19:30:00": 1884, "20:00:00": 1884, "20:30:00": 1884,
            "21:00:00": 1885, "21:30:00": 1885, "22:00:00": 1885,
            "22:30:00": 1885
        }
    },
    "112":{
        "name":"Diamond Plaza, Jessore Road",
        "slots":{
            "12:00:00": 489, "12:30:00": 489, "13:00:00": 489,
            "13:30:00": 489, "14:00:00": 489, "14:30:00": 490,
            "15:00:00": 490, "15:30:00": 490, "16:00:00": 490,
            "16:30:00": 490, "17:00:00": 490, "17:30:00": 490,
            "18:00:00": 490, "18:30:00": 491, "19:00:00": 491,
            "19:30:00": 491, "20:00:00": 491, "20:30:00": 491,
            "21:00:00": 1095, "21:30:00": 1095, "22:00:00": 1095,
            "22:30:00": 1095
        }
    },
    "53":{
        "name":"Park Street",
        "slots":{
            "12:00:00": 207, "12:30:00": 207, "13:00:00": 207,
            "13:30:00": 207, "14:00:00": 207, "14:30:00": 208,
            "15:00:00": 208, "15:30:00": 208, "16:00:00": 208,
            "16:30:00": 208, "17:00:00": 208, "17:30:00": 208,
            "18:00:00": 208, "18:30:00": 209, "19:00:00": 209,
            "19:30:00": 209, "20:00:00": 209, "20:30:00": 209,
            "21:00:00": 1098, "21:30:00": 1098, "22:00:00": 1098,
            "22:30:00": 1098
        }
    },
    "224":{
        "name":"Acropolis Mall, East Kolkata Township",
        "slots":{
            "12:00:00": 1654, "12:30:00": 1654, "13:00:00": 1654,
            "13:30:00": 1654, "14:00:00": 1654, "14:30:00": 1655,
            "15:00:00": 1655, "15:30:00": 1655, "16:00:00": 1655,
            "16:30:00": 1655, "17:00:00": 1655, "17:30:00": 1655,
            "18:00:00": 1655, "18:30:00": 1656, "19:00:00": 1656,
            "19:30:00": 1656, "20:00:00": 1656, "20:30:00": 1656,
            "21:00:00": 1657, "21:30:00": 1657, "22:00:00": 1657,
            "22:30:00": 1657
        }
    },
    "52":{
        "name":"Sector 5, Salt Lake",
        "slots":{
            "12:00:00": 203, "12:30:00": 203, "13:00:00": 203,
            "13:30:00": 203, "14:00:00": 203, "14:30:00": 204,
            "15:00:00": 204, "15:30:00": 204, "16:00:00": 204,
            "16:30:00": 204, "17:00:00": 204, "17:30:00": 204,
            "18:00:00": 204, "18:30:00": 205, "19:00:00": 205,
            "19:30:00": 205, "20:00:00": 205, "20:30:00": 205,
            "21:00:00": 1096, "21:30:00": 1096, "22:00:00": 1096,
            "22:30:00": 1096
        }
    },
    "211":{
        "name":"Jessore Road, Barasat",
        "slots":{
            "12:00:00": 1618, "12:30:00": 1618, "13:00:00": 1618,
            "13:30:00": 1618, "14:00:00": 1618, "14:30:00": 1619,
            "15:00:00": 1619, "15:30:00": 1619, "16:00:00": 1619,
            "16:30:00": 1619, "17:00:00": 1619, "17:30:00": 1619,
            "18:00:00": 1619, "18:30:00": 1620, "19:00:00": 1620,
            "19:30:00": 1620, "20:00:00": 1620, "20:30:00": 1620,
            "21:00:00": 1621, "21:30:00": 1621, "22:00:00": 1621,
            "22:30:00": 1621
        }
    },
    "212":{
        "name":"Westend Mall, Aundh",
        "slots":{
            "12:00:00": 1622, "12:30:00": 1622, "13:00:00": 1622,
            "13:30:00": 1622, "14:00:00": 1622, "14:30:00": 1623,
            "15:00:00": 1623, "15:30:00": 1623, "16:00:00": 1623,
            "16:30:00": 1623, "17:00:00": 1623, "17:30:00": 1623,
            "18:00:00": 1623, "18:30:00": 1624, "19:00:00": 1624,
            "19:30:00": 1624, "20:00:00": 1624, "20:30:00": 1624,
            "21:00:00": 1625, "21:30:00": 1625, "22:00:00": 1625,
            "22:30:00": 1625
        }
    },
    "190":{
        "name":"Elpro Mall, MG Road",
        "slots":{
            "12:00:00": 1375, "12:30:00": 1375, "13:00:00": 1375,
            "13:30:00": 1375, "14:00:00": 1375, "14:30:00": 1376,
            "15:00:00": 1376, "15:30:00": 1376, "16:00:00": 1376,
            "16:30:00": 1376, "17:00:00": 1376, "17:30:00": 1376,
            "18:00:00": 1376, "18:30:00": 1377, "19:00:00": 1377,
            "19:30:00": 1377, "20:00:00": 1377, "20:30:00": 1377,
            "21:00:00": 1378, "21:30:00": 1378, "22:00:00": 1378,
            "22:30:00": 1378
        }
    },
    "51":{
        "name":"ETERNITY MALL, NAGPUR",
        "slots":{
            "12:00:00": 199, "12:30:00": 199, "13:00:00": 199,
            "13:30:00": 199, "14:00:00": 199, "14:30:00": 200,
            "15:00:00": 200, "15:30:00": 200, "16:00:00": 200,
            "16:30:00": 200, "17:00:00": 200, "17:30:00": 200,
            "18:00:00": 200, "18:30:00": 201, "19:00:00": 201,
            "19:30:00": 201, "20:00:00": 201, "20:30:00": 201,
            "21:00:00": 202, "21:30:00": 202, "22:00:00": 202,
            "22:30:00": 202
        }
    },
    "58":{
        "name":"Sayaji Hotel, Wakad",
        "slots":{
            "12:00:00": 227, "12:30:00": 227, "13:00:00": 227,
            "13:30:00": 227, "14:00:00": 227, "14:30:00": 228,
            "15:00:00": 228, "15:30:00": 228, "16:00:00": 228,
            "16:30:00": 228, "17:00:00": 228, "17:30:00": 228,
            "18:00:00": 228, "18:30:00": 229, "19:00:00": 229,
            "19:30:00": 229, "20:00:00": 229, "20:30:00": 229,
            "21:00:00": 230, "21:30:00": 230, "22:00:00": 230,
            "22:30:00": 230
        }
    },
    "407":{
        "name":"Times Square, Sakinaka",
        "slots":{
            "12:00:00": 1763, "12:30:00": 1763, "13:00:00": 227,
            "13:30:00": 1763, "14:00:00": 1763, "14:30:00": 1764,
            "15:00:00": 1764, "15:30:00": 1764, "16:00:00": 1764,
            "16:30:00": 1764, "17:00:00": 1764, "17:30:00": 1764,
            "18:00:00": 1764, "18:30:00": 1765, "19:00:00": 1765,
            "19:30:00": 1765, "20:00:00": 1765, "20:30:00": 1765,
            "21:00:00": 1766, "21:30:00": 1766, "22:00:00": 1766,
            "22:30:00": 1766
        }
    },
    "135":{
        "name":"Amanora",
        "slots":{
            "12:00:00": 748, "12:30:00": 748, "13:00:00": 748,
            "13:30:00": 748, "14:00:00": 748, "14:30:00": 749,
            "15:00:00": 749, "15:30:00": 749, "16:00:00": 749,
            "16:30:00": 749, "17:00:00": 749, "17:30:00": 749,
            "18:00:00": 749, "18:30:00": 750, "19:00:00": 750,
            "19:30:00": 750, "20:00:00": 750, "20:30:00": 750,
            "21:00:00": 751, "21:30:00": 751, "22:00:00": 751,
            "22:30:00": 751
        }
    },
    "4":{
        "name":"Sector 11, Belapur",
        "slots":{
            "12:00:00": 4, "12:30:00": 4, "13:00:00": 4,
            "13:30:00": 4, "14:00:00": 4, "14:30:00": 10,
            "15:00:00": 10, "15:30:00": 10, "16:00:00": 10,
            "16:30:00": 10, "17:00:00": 10, "17:30:00": 10,
            "18:00:00": 10, "18:30:00": 16, "19:00:00": 16,
            "19:30:00": 16, "20:00:00": 16, "20:30:00": 16,
            "21:00:00": 22, "21:30:00": 22, "22:00:00": 22,
            "22:30:00": 22
        }
    },
    "55":{
        "name":"Kalyani Nagar",
        "slots":{
            "12:00:00": 215, "12:30:00": 215, "13:00:00": 215,
            "13:30:00": 215, "14:00:00": 215, "14:30:00": 216,
            "15:00:00": 216, "15:30:00": 216, "16:00:00": 216,
            "16:30:00": 216, "17:00:00": 216, "17:30:00": 216,
            "18:00:00": 216, "18:30:00": 217, "19:00:00": 217,
            "19:30:00": 217, "20:00:00": 217, "20:30:00": 217,
            "21:00:00": 218, "21:30:00": 218, "22:00:00": 218,
            "22:30:00": 218
        }
    },
    "35":{
        "name":"Sector 26",
        "slots":{
            "12:00:00": 136, "12:30:00": 136, "13:00:00": 136,
            "13:30:00": 136, "14:00:00": 136, "14:30:00": 137,
            "15:00:00": 137, "15:30:00": 137, "16:00:00": 137,
            "16:30:00": 137, "17:00:00": 137, "17:30:00": 137,
            "18:00:00": 137, "18:30:00": 138, "19:00:00": 138,
            "19:30:00": 138, "20:00:00": 138, "20:30:00": 138,
            "21:00:00": 139, "21:30:00": 139, "22:00:00": 139,
            "22:30:00": 139
        }
    },
    "100":{
        "name":"Ambience Mall, Sector 24",
        "slots":{
            "12:00:00": 447, "12:30:00": 447, "13:00:00": 447,
            "13:30:00": 447, "14:00:00": 447, "14:30:00": 448,
            "15:00:00": 448, "15:30:00": 448, "16:00:00": 448,
            "16:30:00": 448, "17:00:00": 448, "17:30:00": 448,
            "18:00:00": 448, "18:30:00": 449, "19:00:00": 449,
            "19:30:00": 449, "20:00:00": 449, "20:30:00": 449,
            "21:00:00": 450, "21:30:00": 450, "22:00:00": 450,
            "22:30:00": 450
        }
    },
    "123":{
        "name":"Stellar IT Park, Sector 62",
        "slots":{
            "12:00:00": 533, "12:30:00": 533, "13:00:00": 533,
            "13:30:00": 533, "14:00:00": 533, "14:30:00": 534,
            "15:00:00": 534, "15:30:00": 534, "16:00:00": 534,
            "16:30:00": 534, "17:00:00": 534, "17:30:00": 534,
            "18:00:00": 534, "18:30:00": 535, "19:00:00": 535,
            "19:30:00": 535, "20:00:00": 535, "20:30:00": 535,
            "21:00:00": 536, "21:30:00": 536, "22:00:00": 536,
            "22:30:00": 536
        }
    }
}

# ========== FETCH FUNCTION ==========
# def fetch_slots(start_date, days=1):
#     all_slots = []

#     for branch_id, branch_info in branches_config.items():
#         branch_name = branch_info["name"]
#         slot_map = branch_info.get("slots", {

#         })  # contains {"12:00:00": 1105, ...}

#         for d in range(days):
#             date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")

#             # iterate over every time-slot combination
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
#                                 "Branch": branch_name,
#                                 "Branch ID": branch_id,
#                                 "Date": date_str,
#                                 "Slot Time": time_str,
#                                 "Period": b["period"]["periodName"],
#                                 "Customer Type": b["customerType"],
#                                 "Food Type": b["foodType"],
#                                 "Plan": b["displayName"],
#                                 "Price": b["totalAmount"],
#                                 "Original Price": b["originalPrice"],
#                             })
#                     else:
#                         print(f"Error {r.status_code} for {branch_name} ({branch_id}) - {date_str} {time_str}")
#                 except Exception as e:
#                     print(f"Exception fetching {branch_name} ({branch_id}) - {date_str} {time_str}: {e}")

#     return pd.DataFrame(all_slots)


def fetch_slots(start_date, days=1):
    all_slots = []
    total_requests = 0

    progress = st.progress(0, text="Fetching buffet data...")

    for branch_idx, (branch_id, branch_info) in enumerate(branches_config.items(), start=1):
        branch_name = branch_info["name"]
        slot_map = branch_info.get("slots", {})

        for d in range(days):
            date_str = (start_date + timedelta(days=d)).strftime("%Y-%m-%d")

            for i, (time_str, slot_id) in enumerate(slot_map.items(), start=1):
                total_requests += 1
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
                    # ✅ Add timeout + verify JSON
                    r = requests.post(url, json=payload, headers=headers, timeout=10)
                    r.raise_for_status()
                    data = r.json()

                    buffets = (
                        data.get("results", {})
                            .get("buffets", {})
                            .get("buffet_data", [])
                            or []
                    )

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
                    print(f"⚠️ Timeout for {branch_name} ({branch_id}) - {date_str} {time_str}")
                except Exception as e:
                    print(f"❌ Error fetching {branch_name} ({branch_id}) - {date_str} {time_str}: {e}")

                # ✅ Small delay between requests (avoid flooding)
                import time
                time.sleep(0.2)

    progress.empty()
    return pd.DataFrame(all_slots)

# ========== STREAMLIT DASHBOARD ==========
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
st.title("🍽️ Barbeque Nation Buffet Monitor")

# Sidebar Controls
st.sidebar.header("⚙️ Controls")
interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=3000, value=35000, step=30)
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
# changes_detected = False
# if not st.session_state.first_run and not st.session_state.prev_data.empty:
#     # align columns
#     common_cols = [c for c in st.session_state.prev_data.columns if c in df.columns]
#     df_cmp = df[common_cols].reset_index(drop=True)
#     prev_cmp = st.session_state.prev_data[common_cols].reset_index(drop=True)

#     # detect any row-wise difference
#     difference = df_cmp[df_cmp.ne(prev_cmp).any(axis=1)]
#     if not difference.empty:
#         st.session_state.last_changes = difference
#         changes_detected = True
#     else:
#         st.session_state.last_changes = pd.DataFrame()
# else:
#     st.session_state.last_changes = pd.DataFrame()


# ========== CHANGE DETECTION ==========

changes_detected = False

if not st.session_state.first_run and not st.session_state.prev_data.empty:
    df = df.copy()
    prev_df = st.session_state.prev_data.copy()

    # Define unique key for matching rows
    key_cols = ["Branch", "Date", "Period", "Customer Type", "Food Type", "Plan", "Slot Time"]
    df["unique_key"] = df[key_cols].astype(str).agg("_".join, axis=1)
    prev_df["unique_key"] = prev_df[key_cols].astype(str).agg("_".join, axis=1)

    # Merge to find price differences
    merged = df.merge(prev_df, on="unique_key", suffixes=("_new", "_old"), how="left")

    # Detect rows where price or original price changed
    changed_rows = merged[
        (merged["Price_new"] != merged["Price_old"]) |
        (merged["Original Price_new"] != merged["Original Price_old"])
    ]
    
    st.dataframe(changed_rows[[
        "Branch_new", "Date_new", "Slot Time_new",
        "Price_old", "Price_new", "Original Price_old", "Original Price_new"
    ]])


    if not changed_rows.empty:
        st.session_state.last_changes = df[df["unique_key"].isin(changed_rows["unique_key"])]
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
