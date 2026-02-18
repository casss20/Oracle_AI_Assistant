import streamlit as st
import os
import base64
import time
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="The Oracle",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Josefin+Sans:wght@300;400;600;700&family=Special+Elite&display=swap');

    /* Variables based on the vintage design */
    :root {
        --bg-color: #5fa8a0;
        --header-bg: #4a8880;
        --sidebar-bg: #407870; /* Slightly darker for contrast */
        --paper-bg: #f5edd8;
        --paper-alt: #e6dcc0;
        --accent-gold: #d4a843;
        --border-bronze: #8c6a36;
        --text-dark: #2a1a08;
        --text-light: #f5edd8;
        --shadow-color: rgba(42,26,8,0.25);
    }

    /* Global Overrides */
    .stApp {
        background-color: var(--bg-color);
        background-image: linear-gradient(135deg, #5fa8a0 0%, #4a8880 100%);
        font-family: 'Josefin Sans', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--text-light) !important;
        text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── SIDEBAR STYLING ── */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 4px double var(--border-bronze);
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }
    
    /* Sidebar Headers */
    .sidebar-header {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        font-style: italic;
        color: var(--text-light);
        text-align: center;
        padding-bottom: 16px;
        border-bottom: 2px solid rgba(245,237,216,0.2);
        margin-bottom: 24px;
        text-shadow: 1px 1px 0 rgba(0,0,0,0.2);
    }
    
    .sidebar-label {
        font-family: 'Josefin Sans', sans-serif;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--accent-gold);
        margin-bottom: 8px;
        margin-top: 20px;
        text-shadow: 1px 1px 0 rgba(0,0,0,0.2);
    }

    /* Widget Styling */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(42,26,8,0.2);
        border: 1px solid var(--accent-gold);
        color: var(--text-light);
        font-family: 'Special Elite', cursive;
    }
    .stCheckbox label {
        color: #e8d9b8 !important;
        font-family: 'Josefin Sans', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* ── HEADER RIBBON ── */
    .oracle-header {
        text-align: center;
        padding: 20px 0 60px;
        color: var(--text-light);
        position: relative;
    }
    .oracle-title {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 84px;
        letter-spacing: 12px;
        text-transform: uppercase;
        text-shadow: 4px 4px 0 #3a6860, 8px 8px 0 rgba(0,0,0,0.15);
        line-height: 0.9;
        margin: 0;
        background: -webkit-linear-gradient(#f9f1e0, #d4a843);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .ribbon-badge {
        position: relative;
        background: linear-gradient(to bottom, #d4a843, #b88d30);
        color: #422a10;
        padding: 10px 40px;
        font-family: 'Josefin Sans', sans-serif;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 4px;
        text-transform: uppercase;
        box-shadow: 0 4px 12px var(--shadow-color);
        display: inline-block;
        margin-top: 5px;
        border: 1px solid #f9f1e0;
    }
    .ribbon-badge::before, .ribbon-badge::after {
        content: '';
        position: absolute;
        top: 0; bottom: 0;
        width: 20px;
        border: 20px solid #b88d30;
        z-index: -1;
    }
    .ribbon-badge::before {
        left: -15px;
        border-right-color: transparent;
        border-left-color: transparent;
        transform: skewX(-15deg);
    }
    .ribbon-badge::after {
        right: -15px;
        border-left-color: transparent;
        border-right-color: transparent;
        transform: skewX(15deg);
    }

    /* ── CHAT BUBBLES ── */
    .stChatMessage {
        background: transparent !important;
        padding: 1rem 0 !important;
    }
    
    /* User Message */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) .stChatMessageContent {
        background-color: var(--paper-alt) !important;
        color: #2a1a08 !important;
        border-radius: 2px !important;
        border: 1px solid var(--border-bronze) !important;
        box-shadow: 2px 2px 4px var(--shadow-color);
        font-family: 'Special Elite', cursive;
        position: relative;
        transform: rotate(-0.5deg);
    }
    /* "Stamp" effect for user */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) .stChatMessageContent::after {
        content: '✉';
        position: absolute;
        top: -10px;
        right: -5px;
        color: var(--border-bronze);
        font-size: 20px;
        opacity: 0.5;
        transform: rotate(15deg);
    }

    /* Oracle Message */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) .stChatMessageContent {
        background-color: var(--paper-bg) !important;
        color: #2a1a08 !important;
        border-radius: 2px !important;
        border: 1px solid var(--border-bronze) !important;
        border-left: 4px solid var(--accent-gold) !important; /* Accent bar */
        box-shadow: 3px 3px 6px var(--shadow-color);
        font-family: 'Playfair Display', serif; /* More formal for Oracle */
        font-size: 17px;
        line-height: 1.6;
    }

    /* ── INPUTS ── */
    .stChatInput textarea, .stTextArea textarea {
        background-color: var(--paper-bg) !important;
        border: 2px solid var(--border-bronze) !important;
        border-radius: 4px;
        font-family: 'Special Elite', cursive !important;
        font-size: 16px !important;
        color: var(--text-dark) !important;
        box-shadow: inset 2px 2px 6px rgba(0,0,0,0.1);
    }
    .stChatInput textarea:focus, .stTextArea textarea:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 2px rgba(212,168,67,0.4) !important;
    }

    /* ── CARDS ── */
    .vintage-card {
        background: var(--paper-bg);
        border: 1px solid var(--border-bronze);
        padding: 4px; /* Double border effect frame */
        box-shadow: 8px 8px 0 rgba(0,0,0,0.2);
        margin-bottom: 24px;
        position: relative;
    }
    .vintage-card-inner {
        border: 1px solid var(--border-bronze);
        height: 100%;
    }
    
    /* Rivets */
    .vintage-card::before, .vintage-card::after {
        content: '•';
        color: var(--border-bronze);
        position: absolute;
        font-size: 20px;
        line-height: 10px;
    }
    .vintage-card::before { top: 4px; left: 6px; }
    .vintage-card::after { top: 4px; right: 6px; }

    .vintage-card-header {
        background: var(--header-bg); /* Use header teal for contrast */
        padding: 12px 18px;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--text-light);
        border-bottom: 2px solid var(--border-bronze);
        text-align: center;
    }
    .vintage-card-body {
        padding: 18px;
        background-color: var(--paper-bg);
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background: linear-gradient(to bottom, #d4a843, #c09030) !important;
        border: 1px solid #8c6a36 !important;
        border-bottom: 3px solid #8c6a36 !important;
        color: #422a10 !important;
        font-family: 'Josefin Sans', sans-serif !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border-radius: 2px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        transition: all 0.1s !important;
        padding: 0.6rem 1.2rem !important;
        text-shadow: 0 1px 0 rgba(255,255,255,0.3);
    }
    .stButton > button:hover {
        transform: translateY(1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        border-bottom-width: 2px !important;
        background: linear-gradient(to bottom, #deb850, #d4a843) !important;
    }
    .stButton > button:active {
        transform: translateY(3px) !important;
        box-shadow: none !important;
        border-bottom-width: 1px !important;
    }
    
    /* ── STATS ── */
    div[data-testid="stMetric"] {
        background-color: rgba(245,237,216,0.9);
        border: 2px solid var(--border-bronze);
        border-radius: 2px;
        padding: 10px;
        text-align: center;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.15);
    }
    label[data-testid="stMetricLabel"] {
        font-family: 'Josefin Sans', sans-serif;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: var(--border-bronze) !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif;
        font-size: 32px !important;
        font-weight: 900 !important;
        color: var(--text-dark) !important;
    }
</style>
""", unsafe_allow_html=True)

# ── LOGIC SETUP ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Greetings, traveler. I am The Oracle. Ask me anything — I shall consult the archives of the known world on your behalf."}
    ]
if "video_history" not in st.session_state:
    st.session_state.video_history = []
if "did_key" not in st.session_state:
    raw_key = os.getenv("DID_API_KEY")
    st.session_state.did_key = base64.b64encode(f"{raw_key}:".encode()).decode() if raw_key else None

VOICES = {
    "Jenny — US Female": "en-US-JennyNeural",
    "Guy — US Male": "en-US-GuyNeural",
    "Aria — US Female": "en-US-AriaNeural",
    "Sonia — UK Female": "en-GB-SoniaNeural",
    "Ryan — UK Male": "en-GB-RyanNeural",
}

@st.cache_resource
def setup_agent():
    try:
        llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
        tools = [
            Tool(
                name="Google Search",
                func=search.run,
                description="Search Google for current information"
            )
        ]
        # Oracle Persona Prompt
        prompt = PromptTemplate.from_template("""You are The Oracle — a wise, eloquent vintage AI assistant. Speak with measured authority, subtle warmth, and occasional poetic flourish. Keep responses concise (2-4 sentences) but insightful. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}""")

        agent = create_react_agent(llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)
    except Exception as e:
        st.error(f"Agent setup failed: {e}")
        return None

def create_avatar_video(text, voice_id):
    if not st.session_state.did_key:
        st.error("D-ID API key missing")
        return None

    headers = {
        "Authorization": f"Basic {st.session_state.did_key}",
        "Content-Type": "application/json"
    }
    # Using a vintage-style avatar image if possible, or default
    source_url = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg" 
    
    payload = {
        "script": {
            "type": "text",
            "provider": {"type": "microsoft", "voice_id": voice_id},
            "input": text[:300]
        },
        "source_url": source_url,
        "config": {"result_format": "mp4"}
    }

    try:
        with st.spinner("Developing portrait..."):
            r = requests.post("https://api.d-id.com/talks", headers=headers, json=payload)
            r.raise_for_status()
            talk_id = r.json().get("id")
            
            # Poll for completion
            for _ in range(30):
                time.sleep(1)
                s = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
                s.raise_for_status()
                d = s.json()
                if d.get("status") == "done":
                    return d.get("result_url")
                elif d.get("status") == "error":
                    st.error(f"D-ID Error: {d.get('error')}")
                    return None
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

agent = setup_agent()

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">✦ The Oracle ✦</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-label">Voice Selection</div>', unsafe_allow_html=True)
    selected_voice_label = st.selectbox("Select Voice", options=list(VOICES.keys()), label_visibility="collapsed")
    selected_voice_id = VOICES[selected_voice_label]
    
    st.markdown('<div class="sidebar-label">Options</div>', unsafe_allow_html=True)
    auto_video = st.checkbox("Auto-generate avatar video", value=True)
    
    st.markdown('<div class="sidebar-label">Recent Portraits</div>', unsafe_allow_html=True)
    if st.session_state.video_history:
        for idx, vurl in enumerate(reversed(st.session_state.video_history[-3:])):
            st.markdown(f"""
            <div style="background: rgba(245,237,216,0.1); border: 1px solid rgba(200,169,110,0.3); padding: 8px; margin-bottom: 8px; border-radius: 4px;">
                <a href="{vurl}" target="_blank" style="color: #e8d9b8; text-decoration: none; font-family: 'Special Elite', cursive; font-size: 11px;">
                    ▶ Portrait #{len(st.session_state.video_history) - idx}
                </a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No portraits yet...")
        
    st.markdown("---")
    if st.button("🗑️ Clear Correspondence"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.video_history = []
        st.rerun()

# ── HEADER ────────────────────────────────────────────────
st.markdown("""
<div class="oracle-header">
    <div class="oracle-title">ORACLE</div>
    <div class="ribbon-badge">Vintage AI Assistant</div>
</div>
""", unsafe_allow_html=True)

# ── TWO COLUMN LAYOUT ─────────────────────────────────────
col_chat, col_right = st.columns([3, 2])

# Left Column: Chat
with col_chat:
    st.markdown('<div style="color: rgba(245,237,216,0.65); font-weight: 700; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">Correspondence</div>', unsafe_allow_html=True)
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("video_url"):
                st.video(msg["video_url"])

    # Input
    if user_input := st.chat_input("Send a dispatch to The Oracle..."):
        # 1. Add User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # 2. Process
        with st.chat_message("assistant"):
            with st.spinner("Consulting the archives..."):
                try:
                    # AI Text
                    result = agent.invoke({"input": user_input})
                    answer = result["output"]
                    st.markdown(answer)
                    
                    # Video Generation
                    video_url = None
                    if auto_video and st.session_state.did_key:
                        video_url = create_avatar_video(answer, selected_voice_id)
                        if video_url:
                            st.video(video_url)
                            st.session_state.video_history.append(video_url)
                    
                    # Save history
                    msg_data = {"role": "assistant", "content": answer}
                    if video_url:
                        msg_data["video_url"] = video_url
                    st.session_state.messages.append(msg_data)
                    
                except Exception as e:
                    st.error(f"The Oracle is silent: {e}")

# Right Column: Portrait Studio
with col_right:
    st.markdown('<div style="color: rgba(245,237,216,0.65); font-weight: 700; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;">Portrait Studio</div>', unsafe_allow_html=True)

    # 1. Live Portrait Card
    st.markdown("""
    <div class="vintage-card">
        <div class="vintage-card-header">◎ Live Portrait</div>
        <div class="vintage-card-body">
    """, unsafe_allow_html=True)
    
    # Show latest video or placeholder
    latest_video = None
    for m in reversed(st.session_state.messages):
        if m.get("video_url"):
            latest_video = m["video_url"]
            break
            
    if latest_video:
        st.video(latest_video)
    else:
        st.markdown("""
        <div style="aspect-ratio: 4/3; background: rgba(125,191,184,0.25); border: 2px dashed rgba(92,61,30,0.2); display: flex; align-items: center; justify-content: center; color: #7a5230; font-size: 11px; font-weight: 700; text-transform: uppercase;">
            Awaiting Portrait
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div></div>", unsafe_allow_html=True)

    # 2. Custom Script Card
    st.markdown("""
    <div class="vintage-card">
        <div class="vintage-card-header">✍ Custom Script</div>
        <div class="vintage-card-body">
    """, unsafe_allow_html=True)
    
    custom_text = st.text_area("Compose message", placeholder="Enter text for the avatar...", label_visibility="collapsed", height=100)
    if st.button("▶ Develop Portrait"):
        if custom_text:
            vurl = create_avatar_video(custom_text, selected_voice_id)
            if vurl:
                st.session_state.video_history.append(vurl)
                st.success("Portrait developed.")
                st.rerun()
        else:
            st.warning("Please enter text.")
            
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # 3. Stats
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Dispatches", len(st.session_state.messages))
    with col_stat2:
        st.metric("Portraits", len(st.session_state.video_history))

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 40px 0; font-family: 'Josefin Sans', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: rgba(245,237,216,0.28);">
    ✦ &nbsp; The Oracle &nbsp; — &nbsp; Est. MMXXV &nbsp; ✦
</div>
""", unsafe_allow_html=True)