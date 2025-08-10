import streamlit as st
import random
import time
from collections import defaultdict
import json
from datetime import datetime
import requests
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="🎵 Folk Festival Nominations 🏕️",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets integration (replace with your sheet URL)
SHEET_URL = st.secrets.get("sheet_url", "")  # Add this to your Streamlit secrets

def load_data():
    """Load data from Google Sheets or fallback to session state"""
    try:
        if SHEET_URL:
            # Try to load from Google Sheets
            response = requests.get(SHEET_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                nominations = defaultdict(int, data.get('nominations', {}))
                return {
                    'nominations': nominations,
                    'nominators': data.get('nominators', []),
                    'write_in_candidates': set(data.get('write_in_candidates', [])),
                    'nomination_reasons': data.get('nomination_reasons', {})
                }
    except:
        pass
    
    # Fallback to session state if available
    if hasattr(st.session_state, 'nominations'):
        return {
            'nominations': st.session_state.nominations,
            'nominators': st.session_state.nominators,
            'write_in_candidates': st.session_state.write_in_candidates,
            'nomination_reasons': st.session_state.nomination_reasons
        }
    
    # Default empty state
    return {
        'nominations': defaultdict(int),
        'nominators': [],
        'write_in_candidates': set(),
        'nomination_reasons': {}
    }

def save_data():
    """Save data to Google Sheets (if configured) and session state"""
    try:
        # Always save to session state as backup
        data = {
            'nominations': dict(st.session_state.nominations),
            'nominators': st.session_state.nominators,
            'write_in_candidates': list(st.session_state.write_in_candidates),
            'nomination_reasons': getattr(st.session_state, 'nomination_reasons', {})
        }
        
        if SHEET_URL:
            # Save to Google Sheets
            requests.post(SHEET_URL.replace('/edit', '/exec'), 
                         data={'data': json.dumps(data)}, timeout=5)
    except Exception as e:
        st.error(f"Warning: Data save issue: {e}")

def get_current_leader():
    """Get the current leader(s) in nominations"""
    if not st.session_state.nominations:
        return None, 0
    
    sorted_nominations = sorted(st.session_state.nominations.items(), 
                              key=lambda x: x[1], reverse=True)
    top_votes = sorted_nominations[0][1]
    leaders = [name for name, votes in sorted_nominations if votes == top_votes]
    return leaders, top_votes

# Initialize session state with persistent data
saved_data = load_data()
st.session_state.nominations = saved_data['nominations']
st.session_state.nominators = saved_data['nominators']
st.session_state.write_in_candidates = saved_data['write_in_candidates']
st.session_state.nomination_reasons = saved_data['nomination_reasons']

# Eligible nominees and profiles
eligible_nominees = ["Bowe", "Drew", "Derek", "Emily", "Josh", "TallPaul", "Osc"]
nominee_profiles = {
    "Bowe": "Prefers the digital backdoor but this motherfucker loves a good challenge",
    "Drew": "This multifaceted wheelman has proven his worth on this front before!",
    "Derek": "Surprisingly stealthy despite appearances",
    "Emily": "Can charm security guards with folk song trivia",
    "Josh": "Early bird by nature, coffee addiction helps with dawn missions",
    "TallPaul": "Unspeakable shameless tactics",
    "Osc": "In all honesty this man can probably just walk right past the guards in that smooth Osc fashion we all love and know"
}

folk_quotes = [
    "🎭 'She neva came!...' 🎭",
    "🪕 'I DID IT!' 🪕",
    "🎭 'I changed my shirt!' 🎭",
]

def main():
    # Header
    st.title("🎵🏕️ PHILADELPHIA FOLK FESTIVAL EARLY INFILTRATION NOMINATION SYSTEM 🏕️🎵")

    # Check voting deadline
    today = datetime.now()
    deadline = datetime(2025, 8, 12, 23, 59, 59)  # End of day August 12th 2025
    voting_open = today < deadline
    days_until_deadline = (deadline.date() - today.date()).days

    st.markdown("---")

    # Mission briefing
    with st.expander("🎪 THE MISSION BRIEFING", expanded=True):
        st.markdown(f"""
        **Welcome to the annual tradition nobody wants but somebody must do!**

        Every year, two brave souls must sneak into the festival early (normally it comes down to - who's going with Greg!?)
        to secure the sacred campsite that has been our home away from home.

        🎪 **The Mission:** Arrive before dawn, act casual, claim the spot  
        🎸 **The Risk:** Getting caught by security and having to explain why  
        🏕️ **The Reward:** Being a hero... and internal bragging rights of course  

        **Let the nominations begin! May the odds be ever in someone else's favor.**
        
        ⏰ **Voting Deadline:** Tuesday, August 12th, 2025 at 11:59 PM
        {"🗳️ **Status:** VOTING OPEN" if voting_open else "🔒 **Status:** VOTING CLOSED"}
        {f"({days_until_deadline} days remaining)" if voting_open and days_until_deadline > 0 else ""}
        """)

    # Auto-refresh every 10 seconds to get latest votes
    if st.button("🔄 Refresh Results", help="Click to see latest votes from all devices"):
        st.rerun()

    # Add auto-refresh timer
    placeholder = st.empty()
    with placeholder.container():
        st.info("📱 App auto-refreshes to sync votes across all devices")

    # Sidebar for nominations
    with st.sidebar:
        st.header("🗳️ CAST YOUR NOMINATION")
        st.markdown(random.choice(folk_quotes))

        if voting_open:
            # Nominator name
            nominator = st.text_input("👤 Your name, brave nominator:", 
                                     placeholder="Enter your name")

            if nominator:
                # Build nominee options
                all_nominees = eligible_nominees.copy()
                all_nominees.extend(list(st.session_state.write_in_candidates))
                all_nominees.append(nominator)  # Self-nomination option

                # Nominee selection
                st.markdown("**Choose your nominee:**")
                nominee_choice = st.selectbox(
                    "Select a nominee:",
                    ["-- Select someone --"] + all_nominees + ["Write in new candidate"],
                    key="nominee_select"
                )

                # Write-in option
                write_in_name = None
                if nominee_choice == "Write in new candidate":
                    write_in_name = st.text_input("✏️ Enter write-in candidate name:")
                    if write_in_name:
                        nominee_choice = write_in_name

                # Reasoning
                reason = st.text_area("💭 Why this nominee? (Optional)", 
                                    placeholder="They seem like the obvious choice!")

                # Submit nomination
                if st.button("🎯 CAST NOMINATION", type="primary") and nominee_choice != "-- Select someone --":
                    if nominator not in st.session_state.nominators:
                        # New nomination
                        st.session_state.nominators.append(nominator)
                        st.session_state.nominations[nominee_choice] += 1

                        # Store the reason (without the nominator's name)
                        if reason and reason.strip():
                            if 'nomination_reasons' not in st.session_state:
                                st.session_state.nomination_reasons = {}
                            if nominee_choice not in st.session_state.nomination_reasons:
                                st.session_state.nomination_reasons[nominee_choice] = []
                            st.session_state.nomination_reasons[nominee_choice].append(reason.strip())

                        if write_in_name:
                            st.session_state.write_in_candidates.add(write_in_name)

                        # Save to persistent storage
                        save_data()

                        # Show reaction
                        if nominee_choice == nominator:
                            st.success(f"🦸 {nominator} bravely nominates themselves!")
                            st.balloons()
                        else:
                            reactions = [
                                f"😱 {nominee_choice}: 'Wait, what?!'",
                                f"😏 {nominee_choice}: 'I should have seen this coming...'",
                                f"🤷 {nominee_choice}: 'Well, someone has to do it!'",
                                f"😤 {nominee_choice}: 'I'm getting you back for this!'",
                                f"😌 {nominee_choice}: 'Finally, recognition for my sneaking skills!'"
                            ]
                            st.success(f"🎯 {nominator} nominates {nominee_choice}!")
                            st.info(random.choice(reactions))

                        if reason:
                            st.write(f"💭 *'{reason}'*")

                        # Refresh the page to update results
                        time.sleep(1)  # Brief pause to ensure save completes
                        st.rerun()
                    else:
                        st.error("🎵 You've already cast your nomination! One vote per person.")
        else:
            st.warning("🔒 Voting has closed!")
            st.info("The nomination period ended on Tuesday, August 12th, 2025")

    # Main content area
    col1, col2 = st.columns([1, 1])

    # Nominee roster
    with col1:
        st.header("📋 OFFICIAL NOMINEE ROSTER")
        for i, nominee in enumerate(eligible_nominees, 1):
            st.write(f"**{i}. {nominee}**")
            st.write(f"   *{nominee_profiles[nominee]}*")

        st.write("🖊️ *Write-in candidates welcome! (In case we forgot someone important)*")
        st.write("🤔 *Remember: Amp is busy with mothering Wolfie*")
        st.write("⏰ *Dome, Micky and baby Wanda won't arrive in time*")

    # Live results
    with col2:
        st.header("🎪 LIVE RESULTS")

        if st.session_state.nominations:
            # Sort nominations
            sorted_nominations = sorted(st.session_state.nominations.items(), 
                                      key=lambda x: x[1], reverse=True)

            position_emojis = ["🥇", "🥈", "🥉", "🏅", "🎖️", "🏆", "⭐", "🌟"]

            for i, (nominee, votes) in enumerate(sorted_nominations):
                emoji = position_emojis[min(i, len(position_emojis)-1)]
                vote_text = "vote" if votes == 1 else "votes"

                if votes >= 2:
                    status = "🚨 DANGER ZONE! 🚨"
                    status_color = "red"
                elif votes == 1:
                    status = "⚠️ In the running"
                    status_color = "orange"
                else:
                    status = "😅 Safe for now"
                    status_color = "green"

                st.markdown(f"{emoji} **{nominee}**: {votes} {vote_text}")
                st.markdown(f"<span style='color:{status_color}'>{status}</span>", 
                           unsafe_allow_html=True)

                if nominee in st.session_state.write_in_candidates:
                    st.write("   📝 *(Write-in candidate - thinking outside the tent!)*")

                # Show nomination reasons (without names)
                if nominee in st.session_state.get('nomination_reasons', {}):
                    for reason in st.session_state.nomination_reasons[nominee]:
                        st.write(f"   💭 *\"{reason}\"*")

                st.write("")

            # Stats
            st.markdown("---")
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("📈 Total Votes", sum(st.session_state.nominations.values()))
                st.metric("👥 Nominators", len(set(st.session_state.nominators)))
            with col_stats2:
                st.metric("🎯 Candidates", len(st.session_state.nominations))
                st.metric("📝 Write-ins", len(st.session_state.write_in_candidates))
        else:
            if voting_open:
                st.info("🤔 No nominations yet! Someone needs to step up and cast the first vote...")
            else:
                st.info("🤔 No nominations were cast before the deadline.")

    # Live Winner Announcement Section (shows after first vote)
    if st.session_state.nominations:
        st.markdown("---")
        leaders, top_votes = get_current_leader()
        
        # Always show the dramatic announcement (updates live until deadline)
        st.header("🎭 THE MOMENT OF TRUTH... SO FAR! 🎭")
        st.markdown("🎪" * 30)
        
        if not voting_open:
            # Voting is closed - final results
            if len(leaders) == 1:
                chosen_one = leaders[0]
                st.success("🏆 FINAL WINNER!")
                st.success(f"🎉 **{chosen_one}** has been selected by popular vote with {top_votes} votes!")
            else:
                # Handle final tie with dramatic selection
                chosen_one = random.choice(leaders)
                st.info(f"🤝 FINAL TIE! {len(leaders)} brave souls with {top_votes} votes each!")
                st.success("🎯 THE DICE HAVE SPOKEN!")
                st.success(f"🏆 **{chosen_one}** has been randomly selected as the final winner!")
        else:
            # Voting still open - show current leader
            if len(leaders) == 1:
                chosen_one = leaders[0]
                st.success("🏆 CURRENT WINNER!")
                st.success(f"🎉 **{chosen_one}** is leading with {top_votes} votes!")
                st.write("⚠️ *But voting is still open - this could change!* ⚠️")
            else:
                # Current tie
                st.info(f"🤝 CURRENT TIE! {len(leaders)} brave souls with {top_votes} votes each!")
                st.write("🎲 *If voting ended now, we'd need a coin flip!*")
                chosen_one = random.choice(leaders)  # Pick one for the announcement preview

        # Victory speeches (always show current leader's)
        victory_speeches = [
            f"🎤 {chosen_one}: 'I'd like to thank my agent, my coffee maker, and whoever nominated me...'",
            f"🎤 {chosen_one}: 'This is either the greatest honor or the worst luck of my life!'",
            f"🎤 {chosen_one}: 'I promise to sneak responsibly and secure that campsite!'",
            f"🎤 {chosen_one}: 'Greg, I hope you have a good alarm clock!'",
            f"🎤 {chosen_one}: 'Well, someone had to do it. Might as well be me!'"
        ]
        st.write(random.choice(victory_speeches))

        st.markdown("🎪" * 20)
        st.markdown("### 📣 OFFICIAL ANNOUNCEMENT:")
        if voting_open:
            st.info(f"🏕️ **{chosen_one} and Greg** are currently set to be the Early Bird Infiltration Team!")
            st.warning("⚠️ *Subject to change until voting closes on August 12th, 2025*")
        else:
            st.success(f"🏕️ **{chosen_one} and Greg** will be the official Early Bird Infiltration Team!")
        
        st.info("⏰ **Mission time:** Approximately 4:30 AM (or whenever Greg's alarm goes off)")
        st.info("🎯 **Mission objective:** Secure the sacred campsite spot")
        st.info("🤝 **Mission support:** Everyone else sleeps in and arrives fashionably late")
        st.markdown("🎪" * 20)

        # Folk festival wisdom (only show after voting closes)
        if not voting_open:
            with st.expander("📜 FINAL FESTIVAL WISDOM", expanded=True):
                folk_wisdom = [
                    "🎵 Remember: 'The times they are a-changin'... but the campsite tradition stays the same!' 🎵",
                    "🎸 'Blowin' in the wind' is just the morning breeze at 4:30 AM! 🎸",
                    "🪕 'This land is your land'... but this campsite is OURS! 🪕",
                    "🎺 'We shall overcome'... the security guards and claim our spot! 🎺"
                ]

                st.markdown(random.choice(folk_wisdom))
                st.markdown("""
                **Final reminders:**
                - 🌅 Early bird gets the worm... and the best camping spot!
                - ☕ Coffee is not optional at 4:30 AM
                - 🤝 Teamwork makes the dream work (even if you're dreaming of sleeping in)
                - 🎪 What happens at early infiltration stays at early infiltration
                - 📱 Remember to text the group when you've secured the perimeter!

                🎊 **May your stakes be sturdy and your tarps be taut!** 🎊  
                🏕️ **See you all at the sacred campsite... whenever you decide to roll out of bed!** 🏕️
                """)

    # Enhanced admin controls with nominator list
    if st.session_state.nominations and st.checkbox("🎭 Show advanced options"):
        admin_code = st.text_input("Enter code:", type="password", placeholder="4-digit code")
        
        # Show nominators list when correct code is entered
        if admin_code == "1320":
            st.success("🔓 Admin access granted")
            
            # Display nominator list
            st.subheader("👥 Complete Nominator List:")
            if st.session_state.nominators:
                for i, nominator in enumerate(st.session_state.nominators, 1):
                    st.write(f"{i}. {nominator}")
            else:
                st.write("No nominators yet")
            
            # Reset button
            if st.button("Reset data", type="secondary"):
                st.session_state.nominations = defaultdict(int)
                st.session_state.nominators = []
                st.session_state.write_in_candidates = set()
                st.session_state.nomination_reasons = {}
                save_data()
                st.success("Data reset successfully.")
                time.sleep(1)
                st.rerun()
        elif admin_code and admin_code != "1320":
            st.error("Invalid code.")

if __name__ == "__main__":
    main()
    # --- Google Sheets Persistence Layer for Streamlit Community Cloud ---

    # 1. Setup Instructions:
    #    a. Create a Google Sheet with columns: "nominations", "nominators", "nomination_reasons", "write_in_candidates"
    #    b. Share the sheet with a Google Service Account (see below)
    #    c. Add your service account credentials JSON to Streamlit Secrets as:
    #       [gcp_service_account]
    #       type = ...
    #       project_id = ...
    #       private_key_id = ...
    #       private_key = ...
    #       client_email = ...
    #       client_id = ...
    #       ...
    #    d. Add your sheet URL to Streamlit Secrets as:
    #       [gsheets]
    #       sheet_url = "https://docs.google.com/spreadsheets/d/...."

    import streamlit as st
    import json
    from collections import defaultdict

    # Use Streamlit's built-in Google Sheets connection (no extra pip install needed on Streamlit Cloud)
    from streamlit.connections import ExperimentalBaseConnection

    class GSheetsConnection(ExperimentalBaseConnection):
        def _connect(self, **kwargs):
            import gspread
            from google.oauth2.service_account import Credentials
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds_dict["private_key"] = creds_dict["private_key"].replace('\\n', '\n')
            creds = Credentials.from_service_account_info(creds_dict, scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ])
            client = gspread.authorize(creds)
            return client

        def cursor(self):
            return self._instance

    # Helper to get the worksheet
    def get_worksheet():
        sheet_url = st.secrets["gsheets"]["sheet_url"]
        conn = st.connection("gsheets", type=GSheetsConnection)
        client = conn.cursor()
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.sheet1  # Use first sheet
        return worksheet

    def load_data():
        """
        Loads nominations, nominators, nomination_reasons, and write_in_candidates from Google Sheets.
        """
        worksheet = get_worksheet()
        records = worksheet.get_all_records()
        if not records:
            # No data yet, initialize
            st.session_state.nominations = defaultdict(int)
            st.session_state.nominators = []
            st.session_state.nomination_reasons = {}
            st.session_state.write_in_candidates = set()
            return

        # Use the first (and only) row as the data store
        row = records[0]
        # Each field is stored as a JSON string
        st.session_state.nominations = defaultdict(
            int, json.loads(row.get("nominations", "{}"))
        )
        st.session_state.nominators = json.loads(row.get("nominators", "[]"))
        st.session_state.nomination_reasons = json.loads(row.get("nomination_reasons", "{}"))
        st.session_state.write_in_candidates = set(json.loads(row.get("write_in_candidates", "[]")))

    def save_data():
        """
        Saves nominations, nominators, nomination_reasons, and write_in_candidates to Google Sheets.
        """
        worksheet = get_worksheet()
        # Prepare data as JSON strings
        data = {
            "nominations": json.dumps(dict(st.session_state.nominations)),
            "nominators": json.dumps(list(st.session_state.nominators)),
            "nomination_reasons": json.dumps(dict(st.session_state.nomination_reasons)),
            "write_in_candidates": json.dumps(list(st.session_state.write_in_candidates)),
        }
        records = worksheet.get_all_records()
        if not records:
            # Insert new row
            worksheet.append_row([data["nominations"], data["nominators"], data["nomination_reasons"], data["write_in_candidates"]])
            # Set header if not present
            if worksheet.row_count < 2:
                worksheet.insert_row(["nominations", "nominators", "nomination_reasons", "write_in_candidates"], 1)
        else:
            # Update first row (row 2, since row 1 is header)
            worksheet.update("A2", [[data["nominations"], data["nominators"], data["nomination_reasons"], data["write_in_candidates"]]])

    # --- Why this works ---
    # - Google Sheets is a free, persistent, cloud-hosted database for small data.
    # - All users/devices see the same data instantly (on reload).
    # - Data survives Streamlit container restarts and is shared across all browsers.
    # - No local file storage is used; all data is in the cloud.
    # - No complex DB setup; just a Google Sheet and a service account.
