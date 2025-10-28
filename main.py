def fetch_slots(start_date, days=1):
    all_slots = []
    failed_slots = []
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
                    "branch_id": str(branch_id),
                    "reservation_date": date_str,
                    "reservation_time": time_str,
                    "slot_id": slot_id
                }

                success = False
                last_error = None  # track last actual error
                for attempt in range(3):
                    try:
                        r = requests.post(url, json=payload, headers=headers, timeout=15)
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
                                f"⚠️ No buffet data for {branch_name} ({branch_id}) - {date_str} {time_str}"
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

                    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                        last_error = f"Network/timeout error: {e}"
                        time.sleep(2)
                    except requests.exceptions.RequestException as e:
                        last_error = f"HTTP error: {e} — response: {getattr(e.response, 'text', '')[:200]}"
                        time.sleep(2)
                    except ValueError as e:
                        last_error = f"JSON decode error: {e} — raw text: {r.text[:200] if 'r' in locals() else 'no response'}"
                        break
                    except Exception as e:
                        last_error = f"Unexpected error: {type(e).__name__} — {e}"
                        break

                if not success:
                    failed_slots.append(
                        f"❌ Failed after 3 retries for {branch_name} ({branch_id}) - {date_str} {time_str} | Last error: {last_error}"
                    )

                time.sleep(0.2)

    progress.empty()

    if failed_slots:
        st.warning("Some slots failed to fetch:")
        for msg in failed_slots:
            st.write(msg)

    return pd.DataFrame(all_slots)
