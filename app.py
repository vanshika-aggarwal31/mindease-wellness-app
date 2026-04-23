import streamlit as st
import google.generativeai as genai
from datetime import datetime
import random

# ========== CONFIG ==========
st.set_page_config(
    page_title="MindEase",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== API KEY ==========
GEMINI_API_KEY = "AIzaSyA-m_ip-OISbpVq-r2tFmI_aTCaaei8Gq4"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ========== THEME ==========
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if st.session_state.theme == "light":
    bg = "#FFF5F0"
    card = "#FFFFFF"
    text = "#3D2B1F"
    accent = "#D85A30"
    soft = "#FFE8DF"
else:
    bg = "#1A0F0A"
    card = "#2C1810"
    text = "#FFE8DF"
    accent = "#F0997B"
    soft = "#3D2010"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg}; }}
    .main {{ background-color: {bg}; }}
    [data-testid="stSidebar"] {{ background-color: {soft}; }}
    h1, h2, h3 {{ color: {accent} !important; }}
    p, label {{ color: {text} !important; }}
    .card {{
        background: {card};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid {soft};
    }}
    .chat-user {{
        background: {accent};
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        font-size: 14px;
    }}
    .chat-ai {{
        background: {soft};
        color: {text};
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 75%;
        font-size: 14px;
    }}
    .mood-btn {{
        font-size: 28px;
        background: none;
        border: none;
        cursor: pointer;
    }}
    div[data-testid="stButton"] button {{
        background-color: {accent};
        color: white;
        border-radius: 25px;
        border: none;
        padding: 8px 24px;
        font-weight: 500;
    }}
    div[data-testid="stButton"] button:hover {{
        opacity: 0.85;
    }}
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

# ========== LOGIN PAGE ==========
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card' style='text-align:center; padding: 40px;'>
            <h1 style='font-size:48px; margin:0;'>🌸</h1>
            <h2>MindEase</h2>
            <p style='color:{text}; font-size:16px;'>Your mental wellness companion</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            name = st.text_input("Name", placeholder="Vanshika", key="login_name")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            if st.button("Sign In 🌸", use_container_width=True):
                if name and password:
                    st.session_state.logged_in = True
                    st.session_state.username = name
                    st.rerun()
                else:
                    st.error("Please fill all fields!")

        with tab2:
            new_name = st.text_input("Your name", placeholder="Vanshika", key="signup_name")
            new_email = st.text_input("Email", placeholder="you@email.com", key="signup_email")
            new_pass = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pass")
            if st.button("Create Account 🌸", use_container_width=True):
                if new_name and new_email and new_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = new_name
                    st.rerun()
                else:
                    st.error("Please fill all fields!")

# ========== SIDEBAR ==========
def sidebar():
    with st.sidebar:
        st.markdown(f"<h2 style='color:{accent}'>🌸 MindEase</h2>", unsafe_allow_html=True)
        st.markdown(f"<p>Hello, <b>{st.session_state.username}</b> 👋</p>", unsafe_allow_html=True)
        st.markdown("---")

        page = st.radio("Navigate", [
            "🏠 Home",
            "💬 AI Chat",
            "🌬️ Breathe",
            "📔 Journal",
            "😊 Mood Tracker",
            "✨ Affirmations",
            "⚙️ Settings"
        ])

        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        return page

# ========== HOME PAGE ==========
def home_page():
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
        emoji = "☀️"
    elif hour < 17:
        greeting = "Good Afternoon"
        emoji = "🌤️"
    else:
        greeting = "Good Evening"
        emoji = "🌙"

    st.markdown(f"<h1>{emoji} {greeting}, {st.session_state.username}!</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px; color:{text}'>How are you feeling today?</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class='card' style='text-align:center'>
            <h3>💬 AI Chat</h3>
            <p>Talk to your wellness companion</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='card' style='text-align:center'>
            <h3>📔 Journal</h3>
            <p>{len(st.session_state.journal_entries)} entries written</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='card' style='text-align:center'>
            <h3>😊 Mood</h3>
            <p>{len(st.session_state.mood_log)} moods logged</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    quotes = [
        "You are stronger than you think. 💪",
        "One step at a time. You've got this. 🌸",
        "It's okay to not be okay. Take it slow. 🌿",
        "Your feelings are valid. 💙",
        "Be kind to yourself today. 🌼",
        "Small progress is still progress. ✨"
    ]
    st.markdown(f"""<div class='card' style='text-align:center; border-left: 4px solid {accent}'>
        <h3>✨ Daily Affirmation</h3>
        <p style='font-size:18px; font-style:italic'>"{random.choice(quotes)}"</p>
    </div>""", unsafe_allow_html=True)

# ========== AI CHAT PAGE ==========
def chat_page():
    st.markdown("<h1>💬 AI Wellness Chat</h1>", unsafe_allow_html=True)
    st.markdown(f"<p>I'm here to listen. Talk to me about anything. 🌸</p>", unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>{msg['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-ai'>🌸 {msg['text']}</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Share what's on your mind...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        with st.spinner("thinking..."):
            try:
                prompt = f"""You are MindEase, a warm, empathetic mental wellness companion. 
                The user's name is {st.session_state.username}. 
                Respond with care, understanding and warmth. Keep responses short (2-3 sentences).
                Be supportive like a good friend. Never give medical advice.
                User says: {user_input}"""
                response = model.generate_content(prompt)
                ai_reply = response.text
            except:
                ai_reply = "I'm here for you. Sometimes things feel overwhelming, but you're not alone. 🌸"
        st.session_state.chat_history.append({"role": "ai", "text": ai_reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

# ========== BREATHE PAGE ==========
def breathe_page():
    st.markdown("<h1>🌬️ Breathing Exercise</h1>", unsafe_allow_html=True)
    st.markdown("<p>Take a moment. Breathe with me. 🌿</p>", unsafe_allow_html=True)

    technique = st.selectbox("Choose technique", [
        "4-7-8 Relaxing breath",
        "Box breathing",
        "Simple deep breath"
    ])

    if technique == "4-7-8 Relaxing breath":
        steps = [("Inhale", 4, "#D85A30"), ("Hold", 7, "#7F77DD"), ("Exhale", 8, "#1D9E75")]
        desc = "Inhale 4s → Hold 7s → Exhale 8s"
    elif technique == "Box breathing":
        steps = [("Inhale", 4, "#D85A30"), ("Hold", 4, "#7F77DD"), ("Exhale", 4, "#1D9E75"), ("Hold", 4, "#F0997B")]
        desc = "Inhale 4s → Hold 4s → Exhale 4s → Hold 4s"
    else:
        steps = [("Inhale", 5, "#D85A30"), ("Exhale", 5, "#1D9E75")]
        desc = "Inhale 5s → Exhale 5s"

    st.markdown(f"<div class='card' style='text-align:center'><p>{desc}</p></div>", unsafe_allow_html=True)

    cols = st.columns(len(steps))
    for i, (name, seconds, color) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div class='card' style='text-align:center; border-top: 4px solid {color}'>
                <h3>{name}</h3>
                <h2 style='color:{color} !important'>{seconds}s</h2>
            </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card' style='text-align:center; padding:40px'>
        <div style='width:120px; height:120px; border-radius:50%; 
             background: linear-gradient(135deg, {accent}, #FFB347);
             margin: 0 auto; display:flex; align-items:center; 
             justify-content:center; font-size:40px;'>
            🌬️
        </div>
        <p style='margin-top:16px'>Close your eyes and follow along...</p>
    </div>""", unsafe_allow_html=True)

# ========== JOURNAL PAGE ==========
def journal_page():
    st.markdown("<h1>📔 My Journal</h1>", unsafe_allow_html=True)
    st.markdown("<p>Write your thoughts freely. This is your safe space. 🌿</p>", unsafe_allow_html=True)

    mood = st.select_slider("How are you feeling?", ["😔 Sad", "😐 Okay", "🙂 Good", "😊 Happy", "🤩 Amazing"])
    entry = st.text_area("Write your thoughts...", placeholder="Today I felt...", height=150)

    if st.button("Save Entry 💾"):
        if entry:
            st.session_state.journal_entries.append({
                "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                "mood": mood,
                "text": entry
            })
            st.success("Entry saved! 🌸")
            st.rerun()
        else:
            st.warning("Please write something first!")

    st.markdown("---")
    st.markdown("<h3>Past Entries</h3>", unsafe_allow_html=True)
    if st.session_state.journal_entries:
        for e in reversed(st.session_state.journal_entries):
            st.markdown(f"""<div class='card'>
                <small style='color:{accent}'>{e['date']} · {e['mood']}</small>
                <p style='margin-top:8px'>{e['text']}</p>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No entries yet. Write your first one! 🌸")

# ========== MOOD TRACKER ==========
def mood_page():
    st.markdown("<h1>😊 Mood Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p>Track how you feel each day. 🌈</p>", unsafe_allow_html=True)

    moods = {"😔 Sad": 1, "😐 Okay": 2, "🙂 Good": 3, "😊 Happy": 4, "🤩 Amazing": 5}

    cols = st.columns(5)
    for i, (mood_name, val) in enumerate(moods.items()):
        with cols[i]:
            if st.button(mood_name, use_container_width=True):
                st.session_state.mood_log.append({
                    "date": datetime.now().strftime("%d %b"),
                    "mood": mood_name,
                    "value": val
                })
                st.success(f"Logged: {mood_name} 🌸")
                st.rerun()

    if st.session_state.mood_log:
        st.markdown("---")
        import pandas as pd
        df = pd.DataFrame(st.session_state.mood_log)
        st.markdown("<h3>Your mood history</h3>", unsafe_allow_html=True)
        st.line_chart(df.set_index("date")["value"])

        st.markdown("<h3>Recent logs</h3>", unsafe_allow_html=True)
        for log in reversed(st.session_state.mood_log[-5:]):
            st.markdown(f"""<div class='card'>
                <b>{log['date']}</b> — {log['mood']}
            </div>""", unsafe_allow_html=True)

# ========== AFFIRMATIONS PAGE ==========
def affirmations_page():
    st.markdown("<h1>✨ Daily Affirmations</h1>", unsafe_allow_html=True)
    st.markdown("<p>Words that heal. 🌸</p>", unsafe_allow_html=True)

    all_quotes = [
        "You are enough, just as you are. 🌸",
        "Every day is a fresh start. 🌅",
        "You deserve love and kindness. 💙",
        "Your feelings are valid. 🌿",
        "You are braver than you believe. 💪",
        "Small steps still move you forward. ✨",
        "It's okay to rest. You don't have to be productive every day. 🌙",
        "You have survived every hard day so far. 🏆",
        "Breathe. This too shall pass. 🍃",
        "You are not alone. 🤝",
        "Be gentle with yourself. 🌼",
        "Progress, not perfection. 🌈"
    ]

    if "fav_quotes" not in st.session_state:
        st.session_state.fav_quotes = []

    if "current_quote" not in st.session_state:
        st.session_state.current_quote = random.choice(all_quotes)

    st.markdown(f"""<div class='card' style='text-align:center; padding:40px; border-left: 4px solid {accent}'>
        <h2 style='font-style:italic'>{st.session_state.current_quote}</h2>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("New affirmation 🔄", use_container_width=True):
            st.session_state.current_quote = random.choice(all_quotes)
            st.rerun()
    with col2:
        if st.button("Save favourite ❤️", use_container_width=True):
            if st.session_state.current_quote not in st.session_state.fav_quotes:
                st.session_state.fav_quotes.append(st.session_state.current_quote)
                st.success("Saved! 🌸")

    if st.session_state.fav_quotes:
        st.markdown("---")
        st.markdown("<h3>Your favourites ❤️</h3>", unsafe_allow_html=True)
        for q in st.session_state.fav_quotes:
            st.markdown(f"<div class='card'>{q}</div>", unsafe_allow_html=True)

# ========== SETTINGS PAGE ==========
def settings_page():
    st.markdown("<h1>⚙️ Settings</h1>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>Theme</h3>", unsafe_allow_html=True)
    theme_choice = st.radio("Choose theme", ["🌸 Light theme", "🌙 Dark theme"])
    if st.button("Apply theme"):
        st.session_state.theme = "light" if "Light" in theme_choice else "dark"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""<div class='card'>
        <h3>About MindEase 🌸</h3>
        <p>Built with Python, Streamlit & Google Gemini API</p>
        <p>Made with love for mental wellness 💙</p>
    </div>""", unsafe_allow_html=True)

# ========== MAIN ==========
if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar()
    if "Home" in page:
        home_page()
    elif "Chat" in page:
        chat_page()
    elif "Breathe" in page:
        breathe_page()
    elif "Journal" in page:
        journal_page()
    elif "Mood" in page:
        mood_page()
    elif "Affirmations" in page:
        affirmations_page()
    elif "Settings" in page:
        settings_page()
        