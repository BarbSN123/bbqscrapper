# # import streamlit as st
# # import pandas as pd
# # import requests
# # from datetime import datetime, timedelta
# # from streamlit_autorefresh import st_autorefresh
# # import time
# # import requests


# # # ========= CONFIG =========
# # st.set_page_config(page_title="Buffet Price Monitor", layout="wide")

# # # live GitHub JSON link
# # # GITHUB_JSON_URL = "https://raw.githubusercontent.com/diyanshu-anand/bbq-data/main/json/buffet_data.json"  Cache issues
# # GITHUB_JSON_URL = f"https://raw.githubusercontent.com/diyanshu-anand/bbq-data/main/json/buffet_data.json?nocache={int(time.time())}"
# # # response = requests.get(url, headers={"Cache-Control": "no-cache"})
# # # data = response.json()

# # st.title("🍽️ Barbeque Nation Buffet Monitor (GitHub Synced)")

# # # ========= SIDEBAR =========
# # st.sidebar.header("⚙️ Controls")
# # interval = st.sidebar.number_input("Auto-refresh interval (seconds)", min_value=60, value=3600, step=30)

# # # ========= AUTO REFRESH =========
# # count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# # # ========= SESSION STATE =========
# # if "prev_data" not in st.session_state:
# #     st.session_state.prev_data = pd.DataFrame()
# # if "last_changes" not in st.session_state:
# #     st.session_state.last_changes = pd.DataFrame()
# # if "last_updated" not in st.session_state:
# #     st.session_state.last_updated = None
# # if "first_run" not in st.session_state:
# #     st.session_state.first_run = True
# # if "log" not in st.session_state:
# #     st.session_state.log = []

# # @st.cache_data(ttl=120)
# # def fetch_from_github():
# #     base_url = "https://raw.githubusercontent.com/diyanshu-anand/bbq-data/refs/heads/main/json/"
# #     files = [
# #         "buffet_data_1.json",
# #         "buffet_data_2.json",
# #         "buffet_data_3.json"
# #     ]

# #     dfs = []
# #     gen_time = "Unknown"

# #     for file in files:
# #         url = f"{base_url}/{file}?nocache={int(time.time())}"
# #         try:
# #             res = requests.get(url)
# #             res.raise_for_status()
# #             raw = res.json()

# #             # Handle both old and new formats
# #             if isinstance(raw, dict) and "records" in raw:
# #                 df = pd.DataFrame(raw["records"])
# #                 gen_time = raw.get("generated_at", gen_time)
# #             else:
# #                 df = pd.DataFrame(raw)

# #             # Convert Date column to datetime for consistency
# #             if "Date" in df.columns:
# #                 df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# #             dfs.append(df)

# #         except Exception as e:
# #             st.warning(f"⚠️ Could not load {file}: {e}")

# #     # Merge all into one DataFrame
# #     if dfs:
# #         full_df = pd.concat(dfs, ignore_index=True)
# #     else:
# #         full_df = pd.DataFrame()

# #     return full_df, gen_time


# # df, generated_at = fetch_from_github()

# # if df.empty:
# #     st.warning("No buffet data found in GitHub file.")
# #     st.stop()

# # # ========= DATE FILTER =========
# # min_date = df["Date"].min()
# # max_date = df["Date"].max()

# # if pd.isna(min_date) or pd.isna(max_date):
# #     min_date = datetime.now().date()
# #     max_date = datetime.now().date() + timedelta(days=30)

# # today = datetime.now().date()

# # # Ensure default value is within range
# # if today < min_date.date():
# #     default_date = min_date.date()
# # elif today > max_date.date():
# #     default_date = max_date.date()
# # else:
# #     default_date = today

# # selected_date = st.sidebar.date_input(
# #     "Select Date",
# #     value=default_date,
# #     min_value=min_date.date(),
# #     max_value=max_date.date()
# # )


# # # Filter by selected date
# # df = df[df["Date"].dt.date == selected_date]

# # # ========= BRANCH FILTER =========
# # branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())
# # selected_branch = st.sidebar.selectbox("Select Branch", branches)

# # if selected_branch != "All Branches":
# #     df = df[df["Branch"] == selected_branch]

# # # ========= CHANGE DETECTION =========
# # changes_detected = False
# # change_messages = []

# # if not st.session_state.first_run and not st.session_state.prev_data.empty:
# #     common_cols = [c for c in st.session_state.prev_data.columns if c in df.columns]
# #     new_data = df[common_cols].reset_index(drop=True)
# #     old_data = st.session_state.prev_data[common_cols].reset_index(drop=True)

# #     # Compare new and old rows
# #     diff_mask = new_data.ne(old_data).any(axis=1)
# #     diff = new_data[diff_mask]

# #     if not diff.empty:
# #         st.session_state.last_changes = diff
# #         changes_detected = True

# #         # Create one-line descriptions
# #         for i in diff.index:
# #             branch = diff.loc[i, "Branch"] if "Branch" in diff.columns else "Unknown Branch"
# #             slot = diff.loc[i, "Slot Time"] if "Slot Time" in diff.columns else "Unknown Time"
# #             date = diff.loc[i, "Date"].strftime("%Y-%m-%d") if "Date" in diff.columns else "Unknown Date"

# #             # msg = f"🔄 Change detected at {branch} — {slot} on {date}"
# #             # change_messages.append(msg)
# #     else:
# #         st.session_state.last_changes = pd.DataFrame()
# # else:
# #     st.session_state.last_changes = pd.DataFrame()
# #     change_messages = []

# # # ========= DISPLAY CHANGE MESSAGES =========
# # if change_messages:
# #     st.markdown("### 🧭 Change Summary")
# #     for msg in change_messages:
# #         st.success(msg)
# #     st.markdown("---")


# # # ========= UPDATE SESSION STATE =========
# # st.session_state.prev_data = df.copy()
# # st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# # st.session_state.first_run = False

# # # ========= UPDATE LOG =========
# # log_entry = f"{st.session_state.last_updated} — {'✅ Changes detected' if changes_detected else 'No change'}"
# # st.session_state.log.insert(0, log_entry)
# # if len(st.session_state.log) > 10:
# #     st.session_state.log = st.session_state.log[:10]

# # # ========= SIDEBAR LOG =========
# # st.sidebar.markdown("### 🕓 Refresh Log")
# # for entry in st.session_state.log:
# #     st.sidebar.write(entry)

# # # ========= DISPLAY =========
# # # st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")
# # # st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
# # # st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

# # # if not st.session_state.last_changes.empty:
# # #     st.markdown("### 🔄 Recently Changed Data")
# # #     st.dataframe(st.session_state.last_changes, use_container_width=True)
# # #     st.markdown("---")

# # # if df.empty:
# # #     st.warning("No data found for the selected date and branch.")
# # # else:
# # #     st.markdown("### 📊 Current Buffet Data")
# # #     st.dataframe(df, use_container_width=True)
# # #     st.write("Total Rows:", len(df))


# # # ========= DISPLAY included with all the dates =========

# # st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")
# # st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
# # st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

# # if not st.session_state.last_changes.empty:
# #     st.markdown("### 🔄 Recently Changed Data")
# #     st.dataframe(st.session_state.last_changes, use_container_width=True)
# #     st.markdown("---")

# # if df.empty:
# #     st.warning("No data found for the selected date and branch.")
# # else:
# #     st.markdown("### 📊 Current Buffet Data (Selected Date)")
# #     st.dataframe(df, use_container_width=True)
# #     st.write("Total Rows:", len(df))

# # # ========= SHOW ALL DATA =========
# # st.markdown("---")
# # st.markdown("## 📆 Complete Buffet Dataset (All Dates)")

# # # Optional branch filter reuse (so same branch filter applies)
# # full_df = fetch_from_github()[0]

# # if selected_branch != "All Branches":
# #     full_df = full_df[full_df["Branch"] == selected_branch]

# # if full_df.empty:
# #     st.warning("No buffet data found for all dates.")
# # else:
# #     st.dataframe(full_df.sort_values(["Date", "Branch"]), use_container_width=True)
# #     st.write("Total Rows (All Dates):", len(full_df))

# # import streamlit as st
# # import pandas as pd
# # import requests
# # from datetime import datetime, timedelta
# # from streamlit_autorefresh import st_autorefresh
# # import time
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart

# # # ========= CONFIG =========
# # st.set_page_config(page_title="Buffet Price Monitor", layout="wide")

# # st.title("🍽️ Barbeque Nation Buffet Monitor")

# # # ========= EMAIL CONFIG =========
# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587

# # EMAIL_SENDER = "mona100975@gmail.com"
# # EMAIL_PASSWORD = "ghdt vdgv bern hgur"
# # EMAIL_RECEIVER = "bbqnation1010@gmail.com"

# # DASHBOARD_LINK = "https://bbqscrapper.streamlit.app/"


# # def send_email(subject, body):

# #     try:
# #         msg = MIMEMultipart()
# #         msg["From"] = EMAIL_SENDER
# #         msg["To"] = EMAIL_RECEIVER
# #         msg["Subject"] = subject

# #         msg.attach(MIMEText(body, "plain"))

# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(EMAIL_SENDER, EMAIL_PASSWORD)

# #         server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
# #         server.quit()

# #     except Exception as e:
# #         print("Email sending failed:", e)


# # # ========= SIDEBAR =========
# # st.sidebar.header("⚙️ Controls")

# # interval = st.sidebar.number_input(
# #     "Auto-refresh interval (seconds)", min_value=60, value=3600, step=30
# # )

# # # ========= AUTO REFRESH =========
# # count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# # # ========= SESSION STATE =========
# # if "prev_data" not in st.session_state:
# #     st.session_state.prev_data = pd.DataFrame()

# # if "last_changes" not in st.session_state:
# #     st.session_state.last_changes = pd.DataFrame()

# # if "last_updated" not in st.session_state:
# #     st.session_state.last_updated = None

# # if "first_run" not in st.session_state:
# #     st.session_state.first_run = True

# # if "log" not in st.session_state:
# #     st.session_state.log = []

# # if "last_generated_at" not in st.session_state:
# #     st.session_state.last_generated_at = None


# # # ========= FETCH DATA =========
# # @st.cache_data(ttl=120)
# # def fetch_from_github():

# #     # base_url = "https://raw.githubusercontent.com/diyanshu-anand/bbq-data/refs/heads/main/json"

# #     # files = [
# #     #     "buffet_data_1.json",
# #     #     "buffet_data_2.json",
# #     #     "buffet_data_3.json",
# #     # ]

# #     base_url = "https://raw.githubusercontent.com/BarbSN123/production_pipeline/main/json"
    
# #     files = [
# #         "buffet_data_1.json",
# #         "buffet_data_2.json",
# #         "buffet_data_3.json",
# #     ]


# #     dfs = []
# #     gen_time = "Unknown"

# #     for file in files:

# #         url = f"{base_url}/{file}?nocache={int(time.time())}"

# #         try:
# #             res = requests.get(url)
# #             res.raise_for_status()
# #             raw = res.json()

# #             if isinstance(raw, dict) and "records" in raw:
# #                 df = pd.DataFrame(raw["records"])
# #                 gen_time = raw.get("generated_at", gen_time)
# #             else:
# #                 df = pd.DataFrame(raw)

# #             if "Date" in df.columns:
# #                 df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# #             dfs.append(df)

# #         except Exception as e:
# #             st.warning(f"⚠️ Could not load {file}: {e}")

# #     if dfs:
# #         full_df = pd.concat(dfs, ignore_index=True)
# #     else:
# #         full_df = pd.DataFrame()

# #     return full_df, gen_time


# # df, generated_at = fetch_from_github()

# # if df.empty:
# #     st.warning("No buffet data found in GitHub file.")
# #     st.stop()


# # # ========= DATE FILTER =========
# # min_date = df["Date"].min()
# # max_date = df["Date"].max()

# # if pd.isna(min_date) or pd.isna(max_date):
# #     min_date = datetime.now().date()
# #     max_date = datetime.now().date() + timedelta(days=30)

# # today = datetime.now().date()

# # if today < min_date.date():
# #     default_date = min_date.date()
# # elif today > max_date.date():
# #     default_date = max_date.date()
# # else:
# #     default_date = today


# # selected_date = st.sidebar.date_input(
# #     "Select Date",
# #     value=default_date,
# #     min_value=min_date.date(),
# #     max_value=max_date.date(),
# # )

# # df = df[df["Date"].dt.date == selected_date]


# # # ========= BRANCH FILTER =========
# # branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())

# # selected_branch = st.sidebar.selectbox("Select Branch", branches)

# # if selected_branch != "All Branches":
# #     df = df[df["Branch"] == selected_branch]


# # # ========= EMAIL NOTIFICATION (ONLY WHEN GENERATED_AT CHANGES) =========

# # if not st.session_state.first_run:

# #     if generated_at != st.session_state.last_generated_at:

# #         body = f"""
# # Price changes detected kindly refer to the below link

# # {DASHBOARD_LINK}
# # """

# #         send_email(
# #             "BBQ Buffet Price Monitor Update",
# #             body,
# #         )

# # # update last generated time
# # st.session_state.last_generated_at = generated_at


# # # ========= UPDATE SESSION STATE =========
# # st.session_state.prev_data = df.copy()
# # st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# # st.session_state.first_run = False


# # # ========= UPDATE LOG =========
# # log_entry = f"{st.session_state.last_updated} — Dataset generated at: {generated_at}"

# # st.session_state.log.insert(0, log_entry)

# # if len(st.session_state.log) > 10:
# #     st.session_state.log = st.session_state.log[:10]


# # # ========= SIDEBAR LOG =========
# # st.sidebar.markdown("### 🕓 Refresh Log")

# # for entry in st.session_state.log:
# #     st.sidebar.write(entry)


# # # ========= DISPLAY =========
# # st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")

# # st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
# # st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

# # if df.empty:
# #     st.warning("No data found for the selected date and branch.")

# # else:
# #     st.markdown("### 📊 Current Buffet Data (Selected Date)")
# #     st.dataframe(df, use_container_width=True)
# #     st.write("Total Rows:", len(df))


# # # ========= SHOW ALL DATA =========
# # st.markdown("---")
# # st.markdown("## 📆 Complete Buffet Dataset (All Dates)")

# # full_df = fetch_from_github()[0]

# # if selected_branch != "All Branches":
# #     full_df = full_df[full_df["Branch"] == selected_branch]

# # if full_df.empty:
# #     st.warning("No buffet data found for all dates")

# # else:
# #     st.dataframe(full_df.sort_values(["Date", "Branch"]), use_container_width=True)
# #     st.write("Total Rows (All Dates):", len(full_df))


# # import streamlit as st
# # import pandas as pd
# # import requests
# # from datetime import datetime, timedelta
# # from streamlit_autorefresh import st_autorefresh
# # import time
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart

# # # ========= CONFIG =========
# # st.set_page_config(page_title="Buffet Price Monitor", layout="wide")

# # st.title("🍽️ Barbeque Nation Buffet Monitor")

# # # ========= EMAIL CONFIG =========
# # SMTP_SERVER = "smtp.gmail.com"
# # SMTP_PORT = 587

# # EMAIL_SENDER = "mona100975@gmail.com"
# # EMAIL_PASSWORD = "ghdt vdgv bern hgur"
# # EMAIL_RECEIVER = "bbqnation1010@gmail.com"

# # DASHBOARD_LINK = "https://bbqscrapper.streamlit.app/"


# # def send_email(subject, body):
# #     try:
# #         msg = MIMEMultipart()
# #         msg["From"] = EMAIL_SENDER
# #         msg["To"] = EMAIL_RECEIVER
# #         msg["Subject"] = subject

# #         msg.attach(MIMEText(body, "plain"))

# #         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
# #         server.starttls()
# #         server.login(EMAIL_SENDER, EMAIL_PASSWORD)

# #         server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
# #         server.quit()

# #     except Exception as e:
# #         print("Email sending failed:", e)


# # # ========= SIDEBAR =========
# # st.sidebar.header("⚙️ Controls")

# # interval = st.sidebar.number_input(
# #     "Auto-refresh interval (seconds)", min_value=60, value=3600, step=30
# # )

# # # 🔄 Manual Refresh Button
# # if st.sidebar.button("🔄 Refresh Now"):
# #     st.cache_data.clear()
# #     st.rerun()

# # # ========= AUTO REFRESH =========
# # count = st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# # # ========= SESSION STATE =========
# # if "prev_data" not in st.session_state:
# #     st.session_state.prev_data = pd.DataFrame()

# # if "last_changes" not in st.session_state:
# #     st.session_state.last_changes = pd.DataFrame()

# # if "last_updated" not in st.session_state:
# #     st.session_state.last_updated = None

# # if "first_run" not in st.session_state:
# #     st.session_state.first_run = True

# # if "log" not in st.session_state:
# #     st.session_state.log = []

# # if "last_generated_at" not in st.session_state:
# #     st.session_state.last_generated_at = None


# # # ========= FETCH DATA =========
# # @st.cache_data(ttl=120)
# # def fetch_from_github():

# #     base_url = "https://raw.githubusercontent.com/BarbSN123/production_pipeline/main/json"

# #     files = [
# #         "buffet_data_1.json",
# #         "buffet_data_2.json",
# #         "buffet_data_3.json",
# #     ]

# #     dfs = []
# #     gen_time = "Unknown"

# #     for file in files:
# #         url = f"{base_url}/{file}?nocache={int(time.time())}"

# #         try:
# #             res = requests.get(url)
# #             res.raise_for_status()
# #             raw = res.json()

# #             if isinstance(raw, dict) and "records" in raw:
# #                 df = pd.DataFrame(raw["records"])
# #                 gen_time = raw.get("generated_at", gen_time)
# #             else:
# #                 df = pd.DataFrame(raw)

# #             if "Date" in df.columns:
# #                 df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# #             dfs.append(df)

# #         except Exception as e:
# #             st.warning(f"⚠️ Could not load {file}: {e}")

# #     if dfs:
# #         full_df = pd.concat(dfs, ignore_index=True)
# #     else:
# #         full_df = pd.DataFrame()

# #     return full_df, gen_time


# # df, generated_at = fetch_from_github()

# # if df.empty:
# #     st.warning("No buffet data found in GitHub file.")
# #     st.stop()

# # #  ADD DAY COLUMN
# # if "Date" in df.columns:
# #     df["Day"] = df["Date"].dt.day_name()

# # # ========= DATE FILTER =========
# # min_date = df["Date"].min()
# # max_date = df["Date"].max()

# # if pd.isna(min_date) or pd.isna(max_date):
# #     min_date = datetime.now().date()
# #     max_date = datetime.now().date() + timedelta(days=30)

# # today = datetime.now().date()

# # if today < min_date.date():
# #     default_date = min_date.date()
# # elif today > max_date.date():
# #     default_date = max_date.date()
# # else:
# #     default_date = today

# # selected_date = st.sidebar.date_input(
# #     "Select Date",
# #     value=default_date,
# #     min_value=min_date.date(),
# #     max_value=max_date.date(),
# # )

# # df = df[df["Date"].dt.date == selected_date]

# # # ========= BRANCH FILTER =========
# # branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())

# # selected_branch = st.sidebar.selectbox("Select Branch", branches)

# # if selected_branch != "All Branches":
# #     df = df[df["Branch"] == selected_branch]

# # # ========= EMAIL NOTIFICATION =========
# # if not st.session_state.first_run:
# #     if generated_at != st.session_state.last_generated_at:
# #         body = f"""
# # Price changes detected kindly refer to the below link

# # {DASHBOARD_LINK}
# # """
# #         send_email("BBQ Buffet Price Monitor Update", body)

# # # update last generated time
# # st.session_state.last_generated_at = generated_at

# # # ========= UPDATE SESSION STATE =========
# # st.session_state.prev_data = df.copy()
# # st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# # st.session_state.first_run = False

# # # ========= UPDATE LOG =========
# # log_entry = f"{st.session_state.last_updated} — Dataset generated at: {generated_at}"

# # st.session_state.log.insert(0, log_entry)

# # if len(st.session_state.log) > 10:
# #     st.session_state.log = st.session_state.log[:10]

# # # ========= SIDEBAR LOG =========
# # st.sidebar.markdown("### 🕓 Refresh Log")

# # for entry in st.session_state.log:
# #     st.sidebar.write(entry)

# # # ========= DISPLAY =========
# # st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")

# # st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
# # st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

# # if df.empty:
# #     st.warning("No data found for the selected date and branch.")
# # else:
# #     st.markdown("### 📊 Current Buffet Data (Selected Date)")
    
# #     # Optional: reorder columns to show Day next to Date
# #     if "Day" in df.columns:
# #         # df = df[["Date", "Day"] + [col for col in df.columns if col not in ["Date", "Day"]]]
# #         # Showing date without time (remove time)
# #         # Format Date (remove time)
# #         df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

# #         df = df[["Date", "Day"] + [col for col in df.columns if col not in ["Date", "Day"]]]

    
# #     st.dataframe(df, use_container_width=True)
# #     st.write("Total Rows:", len(df))

# # # ========= SHOW ALL DATA =========
# # st.markdown("---")
# # st.markdown("## 📆 Complete Buffet Dataset (All Dates)")

# # full_df, _ = fetch_from_github()

# # # ADD DAY COLUMN TO FULL DATA
# # if "Date" in full_df.columns:
# #     full_df["Day"] = full_df["Date"].dt.day_name()

# # if selected_branch != "All Branches":
# #     full_df = full_df[full_df["Branch"] == selected_branch]

# # if full_df.empty:
# #     st.warning("No buffet data found for all dates")
# # else:
# #     # Optional reorder
# #     if "Day" in full_df.columns:
# #         # full_df = full_df[["Date", "Day"] + [col for col in full_df.columns if col not in ["Date", "Day"]]]
# #         # Format Date (remove time)
# #         full_df["Date"] = full_df["Date"].dt.strftime("%Y-%m-%d")

# #         full_df = full_df[["Date", "Day"] + [col for col in full_df.columns if col not in ["Date", "Day"]]]

# #     st.dataframe(full_df.sort_values(["Date", "Branch"]), use_container_width=True)
# #     st.write("Total Rows (All Dates):", len(full_df))

# # Code with Email specific branch updation is done

# import streamlit as st
# import pandas as pd
# import requests
# from datetime import datetime, timedelta
# from streamlit_autorefresh import st_autorefresh
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # ========= CONFIG =========
# st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
# st.title("🍽️ Barbeque Nation Buffet Monitor")

# # ========= EMAIL CONFIG =========
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# EMAIL_SENDER = "mona100975@gmail.com"
# EMAIL_PASSWORD = "ghdt vdgv bern hgur"
# EMAIL_RECEIVER = "bbqnation1010@gmail.com"

# DASHBOARD_LINK = "https://bbqscrapper.streamlit.app/"


# def send_email(subject, body):
#     try:
#         msg = MIMEMultipart()
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = EMAIL_RECEIVER
#         msg["Subject"] = subject

#         msg.attach(MIMEText(body, "plain"))

#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()
#         server.login(EMAIL_SENDER, EMAIL_PASSWORD)

#         server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
#         server.quit()

#     except Exception as e:
#         print("Email sending failed:", e)


# # ========= SIDEBAR =========
# st.sidebar.header("⚙️ Controls")

# interval = st.sidebar.number_input(
#     "Auto-refresh interval (seconds)", min_value=60, value=3600, step=30
# )

# # 🔄 Manual Refresh
# if st.sidebar.button("🔄 Refresh Now"):
#     st.cache_data.clear()
#     st.rerun()

# # ========= AUTO REFRESH =========
# st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# # ========= SESSION STATE =========
# if "prev_data" not in st.session_state:
#     st.session_state.prev_data = pd.DataFrame()

# if "last_generated_at" not in st.session_state:
#     st.session_state.last_generated_at = None

# if "log" not in st.session_state:
#     st.session_state.log = []

# if "last_updated" not in st.session_state:
#     st.session_state.last_updated = None


# # ========= FETCH DATA =========
# @st.cache_data(ttl=120)
# def fetch_from_github():

#     base_url = "https://raw.githubusercontent.com/BarbSN123/production_pipeline/main/json"

#     files = [
#         "buffet_data_1.json",
#         "buffet_data_2.json",
#         "buffet_data_3.json",
#     ]
    
# # Testing Base url and file
#     # base_url = "https://raw.githubusercontent.com/diyanshu-anand/bbq-data/refs/heads/main/"

#     # files = ["buffet_data.json"]

#     dfs = []
#     gen_time = "Unknown"

#     for file in files:
#         url = f"{base_url}/{file}?nocache={int(time.time())}"

#         try:
#             res = requests.get(url)
#             res.raise_for_status()
#             raw = res.json()

#             if isinstance(raw, dict) and "records" in raw:
#                 df = pd.DataFrame(raw["records"])
#                 gen_time = raw.get("generated_at", gen_time)
#             else:
#                 df = pd.DataFrame(raw)

#             if "Date" in df.columns:
#                 df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

#             dfs.append(df)

#         except Exception as e:
#             st.warning(f"⚠️ Could not load {file}: {e}")

#     full_df = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
#     return full_df, gen_time


# # ========= LOAD =========
# df, generated_at = fetch_from_github()

# if df.empty:
#     st.warning("No buffet data found.")
#     st.stop()

# # ========= ADD DAY =========
# df["Day"] = df["Date"].dt.day_name()

# # ========= 🔥 CHANGE DETECTION =========
# changed_branches = []

# if st.session_state.last_generated_at is not None:

#     if generated_at != st.session_state.last_generated_at:

#         prev_df = st.session_state.prev_data.copy()

#         if not prev_df.empty:

#             merged = df.merge(
#                 prev_df,
#                 on=["Branch", "Date"],
#                 how="outer",
#                 suffixes=("_new", "_old"),
#                 indicator=True
#             )
#             # code resulting in value error 
#             # changes = merged[
#             #     (merged["_merge"] != "both") |
#             #     (
#             #         merged.filter(like="_new").fillna("").astype(str)
#             #         != merged.filter(like="_old").fillna("").astype(str)
#             #     ).any(axis=1)
#             # ]

#             # Get comparable columns
#             new_cols = [col for col in merged.columns if col.endswith("_new")]
#             old_cols = [col for col in merged.columns if col.endswith("_old")]

#             # Align column names (remove suffix for comparison)
#             new_df = merged[new_cols].copy()
#             old_df = merged[old_cols].copy()

#             new_df.columns = [col.replace("_new", "") for col in new_cols]
#             old_df.columns = [col.replace("_old", "") for col in old_cols]

#             # Fill NaN and convert to string for safe comparison
#             new_df = new_df.fillna("").astype(str)
#             old_df = old_df.fillna("").astype(str)

#             # Ensure same column order
#             common_cols = new_df.columns.intersection(old_df.columns)
#             new_df = new_df[common_cols]
#             old_df = old_df[common_cols]

#             # Compare safely
#             row_diff = (new_df != old_df).any(axis=1)

#             # Final change detection
#             changes = merged[
#                 (merged["_merge"] != "both") | row_diff
#             ]

#             if not changes.empty:
#                 changed_branches = changes["Branch"].dropna().unique().tolist()

#         # ========= SEND EMAIL =========
#         if changed_branches:
#             branch_list = "\n".join([f"• {b}" for b in changed_branches])

#             body = f"""
# New buffet price updates detected.

# Affected Branches:
# {branch_list}

# Check full details:
# {DASHBOARD_LINK}
# """

#             send_email("🔥 BBQ Price Changes Detected", body)

# # ========= UPDATE STATE =========
# st.session_state.prev_data = df.copy()
# st.session_state.last_generated_at = generated_at
# st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# # ========= LOG =========
# log_entry = f"{st.session_state.last_updated} — Dataset generated at: {generated_at}"
# st.session_state.log.insert(0, log_entry)

# if len(st.session_state.log) > 10:
#     st.session_state.log = st.session_state.log[:10]

# # ========= SIDEBAR LOG =========
# st.sidebar.markdown("### 🕓 Refresh Log")
# for entry in st.session_state.log:
#     st.sidebar.write(entry)

# # ========= DATE FILTER =========
# min_date = df["Date"].min()
# max_date = df["Date"].max()

# selected_date = st.sidebar.date_input(
#     "Select Date",
#     value=datetime.now().date(),
#     min_value=min_date.date(),
#     max_value=max_date.date(),
# )

# df = df[df["Date"].dt.date == selected_date]

# # ========= BRANCH FILTER =========
# branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())
# selected_branch = st.sidebar.selectbox("Select Branch", branches)

# if selected_branch != "All Branches":
#     df = df[df["Branch"] == selected_branch]

# # ========= DISPLAY =========
# st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")

# st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
# st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

# if df.empty:
#     st.warning("No data found.")
# else:
#     st.markdown("### 📊 Current Buffet Data")

#     df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
#     df = df[["Date", "Day"] + [col for col in df.columns if col not in ["Date", "Day"]]]

#     st.dataframe(df, use_container_width=True)
#     st.write("Total Rows:", len(df))

# # ========= FULL DATA =========
# st.markdown("---")
# st.markdown("## 📆 Complete Dataset")

# full_df, _ = fetch_from_github()

# full_df["Day"] = full_df["Date"].dt.day_name()
# full_df["Date"] = full_df["Date"].dt.strftime("%Y-%m-%d")

# if selected_branch != "All Branches":
#     full_df = full_df[full_df["Branch"] == selected_branch]

# full_df = full_df[["Date", "Day"] + [col for col in full_df.columns if col not in ["Date", "Day"]]]

# st.dataframe(full_df.sort_values(["Date", "Branch"]), use_container_width=True)
# st.write("Total Rows (All Dates):", len(full_df))


# Ap crashed solved after 25-03-0205 15:11
#date inconsistency was the issue
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========= CONFIG =========
st.set_page_config(page_title="Buffet Price Monitor", layout="wide")
st.title("🍽️ Barbeque Nation Buffet Monitor")

# ========= EMAIL CONFIG =========
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = "mona100975@gmail.com"
EMAIL_PASSWORD = "ghdt vdgv bern hgur"  # ⚠️ MOVE TO SECRETS LATER
EMAIL_RECEIVER = "bbqnation1010@gmail.com"

DASHBOARD_LINK = "https://bbqscrapper.streamlit.app/"


def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)

        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

    except Exception as e:
        print("Email sending failed:", e)


# ========= SIDEBAR =========
st.sidebar.header("⚙️ Controls")

interval = st.sidebar.number_input(
    "Auto-refresh interval (seconds)", min_value=60, value=3600, step=30
)

if st.sidebar.button("🔄 Refresh Now"):
    st.cache_data.clear()
    st.rerun()

# ========= AUTO REFRESH =========
st_autorefresh(interval * 1000, limit=None, key="buffet_refresh")

# ========= SESSION STATE =========
if "prev_data" not in st.session_state:
    st.session_state.prev_data = pd.DataFrame()

if "last_generated_at" not in st.session_state:
    st.session_state.last_generated_at = None

if "log" not in st.session_state:
    st.session_state.log = []

if "last_updated" not in st.session_state:
    st.session_state.last_updated = None


# ========= FETCH DATA =========
@st.cache_data(ttl=120)
def fetch_from_github():
    # base_url = "https://raw.githubusercontent.com/BarbSN123/production_pipeline/main/json"
    base_url = "https://raw.githubusercontent.com/BarbSN123/bbqscrapper/main"

    files = [
        # "buffet_data_1.json",
        # "buffet_data_2.json",
        # "buffet_data_3.json",
        "buffet_data_part_1.json",
        "buffet_data_part_2.json",
        "buffet_data_part_3.json",
        "buffet_data_part_4.json",
        "buffet_data_part_5.json",
        "buffet_data_part_6.json",
        "buffet_data_part_7.json",
        "buffet_data_part_8.json",
    ]

    dfs = []
    gen_time = "Unknown"

    for file in files:
        url = f"{base_url}/{file}?nocache={int(time.time())}"

        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            raw = res.json()

            if isinstance(raw, dict) and "records" in raw:
                df = pd.DataFrame(raw["records"])
                gen_time = raw.get("generated_at", gen_time)
            else:
                df = pd.DataFrame(raw)

            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df = df.dropna(subset=["Date"])

            dfs.append(df)

        except Exception as e:
            st.warning(f"⚠️ Could not load {file}: {e}")

    if not dfs:
        return pd.DataFrame(), gen_time

    full_df = pd.concat(dfs, ignore_index=True)
    return full_df, gen_time


# ========= LOAD =========
df, generated_at = fetch_from_github()

if df.empty:
    st.warning("No buffet data found.")
    st.stop()

#  SAFE datetime handling
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])
df["Day"] = df["Date"].dt.day_name()

# ========= CHANGE DETECTION =========
changed_branches = []

if st.session_state.last_generated_at is not None:

    if generated_at != st.session_state.last_generated_at:

        prev_df = st.session_state.prev_data.copy()

        if not prev_df.empty:

            merged = df.merge(
                prev_df,
                on=["Branch", "Date"],
                how="outer",
                suffixes=("_new", "_old"),
                indicator=True
            )

            new_cols = [col for col in merged.columns if col.endswith("_new")]
            old_cols = [col for col in merged.columns if col.endswith("_old")]

            new_df = merged[new_cols].copy()
            old_df = merged[old_cols].copy()

            new_df.columns = [col.replace("_new", "") for col in new_cols]
            old_df.columns = [col.replace("_old", "") for col in old_cols]

            new_df = new_df.fillna("").astype(str)
            old_df = old_df.fillna("").astype(str)

            common_cols = new_df.columns.intersection(old_df.columns)
            new_df = new_df[common_cols]
            old_df = old_df[common_cols]

            row_diff = (new_df != old_df).any(axis=1)

            changes = merged[
                (merged["_merge"] != "both") | row_diff
            ]

            if not changes.empty:
                changed_branches = changes["Branch"].dropna().unique().tolist()

        if changed_branches:
            branch_list = "\n".join([f"• {b}" for b in changed_branches])

            body = f"""
New buffet price updates detected.

Affected Branches:
{branch_list}

Check full details:
{DASHBOARD_LINK}
"""

            send_email("🔥 BBQ Price Changes Detected", body)

# ========= UPDATE STATE =========
st.session_state.prev_data = df.copy()
st.session_state.last_generated_at = generated_at
st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ========= LOG =========
log_entry = f"{st.session_state.last_updated} — Dataset generated at: {generated_at}"
st.session_state.log.insert(0, log_entry)

if len(st.session_state.log) > 10:
    st.session_state.log = st.session_state.log[:10]

# ========= SIDEBAR LOG =========
st.sidebar.markdown("### 🕓 Refresh Log")
for entry in st.session_state.log:
    st.sidebar.write(entry)

# ========= DATE FILTER =========
min_date = df["Date"].min()
max_date = df["Date"].max()

selected_date = st.sidebar.date_input(
    "Select Date",
    value=datetime.now().date(),
    min_value=min_date.date(),
    max_value=max_date.date(),
)

df = df[df["Date"].dt.date == selected_date]

# ========= BRANCH FILTER =========
branches = ["All Branches"] + sorted(df["Branch"].dropna().unique().tolist())
selected_branch = st.sidebar.selectbox("Select Branch", branches)

if selected_branch != "All Branches":
    df = df[df["Branch"] == selected_branch]

# ========= DISPLAY =========
st.subheader(f"📅 Viewing Data for: {selected_date.strftime('%Y-%m-%d')}")

st.caption(f"🗂️ Data generated at (from GitHub): {generated_at}")
st.caption(f"💾 Last refreshed: {st.session_state.last_updated}")

if df.empty:
    st.warning("No data found.")
else:
    st.markdown("### 📊 Current Buffet Data")

    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df[["Date", "Day"] + [col for col in df.columns if col not in ["Date", "Day"]]]

    st.dataframe(df, width="stretch")
    st.write("Total Rows:", len(df))

# ========= FULL DATA =========
st.markdown("---")
st.markdown("## 📆 Complete Dataset")

full_df, _ = fetch_from_github()

if full_df.empty:
    st.warning("No complete dataset available.")
    st.stop()

#  SAFE handling again
full_df["Date"] = pd.to_datetime(full_df["Date"], errors="coerce")
full_df = full_df.dropna(subset=["Date"])

full_df["Day"] = full_df["Date"].dt.day_name()
full_df["Date"] = full_df["Date"].dt.strftime("%Y-%m-%d")

if selected_branch != "All Branches":
    full_df = full_df[full_df["Branch"] == selected_branch]

full_df = full_df[["Date", "Day"] + [col for col in full_df.columns if col not in ["Date", "Day"]]]

st.dataframe(full_df.sort_values(["Date", "Branch"]), width="stretch")
st.write("Total Rows (All Dates):", len(full_df))
