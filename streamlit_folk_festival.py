import streamlit as st
import random
import time
from collections import defaultdict
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎵 Folk Festival Nominations 🏕️",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persistent storage functions
DATA_FILE = "folk_festival_data.json"

def load_data():
    """Load data from persistent storage"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                nominations = defaultdict(int, data.get('nominations', {}))
                return {
                    'nominations': nominations,
                    'nominators': data.get('nominators', []),
                    'write_in_candidates': set(data.get('write_in_candidates', [])),
                    'nomination_reasons': data.get('nomination_reasons', {})
                }
        except:
            pass
    
    return {
        'nominations': defaultdict(int),
        'nominators': [],
        'write_in_candidates': set(),
        'nomination_reasons': {}
    }

def save_data():
    """Save current data to persistent storage"""
    try:
        data = {
            'nominations': dict(st.session_state.nominations),
            'nominators': st.session_state.nominators,
            'write_in_candidates': list(st.session_state.write_in_candidates),
            'nomination_reasons': getattr(st.session_state, 'nomination_reasons', {})
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

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
if 'data_loaded' not in st.session_state:
    saved_data = load_data()
    st.session_state.nominations = saved_data['nominations']
    st.session_state.nominators = saved_data['nominators']
    st.session_state.write_in_candidates = saved_data['write_in_candidates']
    st.session_state.nomination_reasons = saved_data['nomination_reasons']
    st.session_state.data_loaded = True
else:
    # Always reload data to get latest votes from other users
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

    # Hidden admin controls (less obvious)
    if st.session_state.nominations and st.checkbox("🎭 Show advanced options"):
        admin_code = st.text_input("Enter code:", type="password", placeholder="4-digit code")
        
        if st.button("Reset data", type="secondary") and admin_code == "1320":
            st.session_state.nominations = defaultdict(int)
            st.session_state.nominators = []
            st.session_state.write_in_candidates = set()
            st.session_state.nomination_reasons = {}
            save_data()
            st.success("Data reset successfully.")
            time.sleep(1)
            st.rerun()
        elif st.button("Reset data", type="secondary"):
            st.error("Invalid code.")

if __name__ == "__main__":
    main()
