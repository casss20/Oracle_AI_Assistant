# streamlit_avatar_app.py
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

load_dotenv()

st.set_page_config(
    page_title="AI Avatar Assistant",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .avatar-video { border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .success-message { padding: 1rem; border-radius: 5px; background-color: #d4edda; color: #155724; }
</style>
""", unsafe_allow_html=True)

st.title("🎬 AI Avatar Assistant")
st.markdown("Ask me anything! I'll search the web and create talking avatar videos.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "video_history" not in st.session_state:
    st.session_state.video_history = []

@st.cache_resource
def setup_did():
    DID_API_KEY = os.getenv("DID_API_KEY")
    if not DID_API_KEY:
        st.error("❌ D-ID API key not found in .env file!")
        return None
    encoded_key = base64.b64encode(f"{DID_API_KEY}:".encode()).decode()
    return encoded_key

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
        
        prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

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
        st.error(f"Error setting up agent: {e}")
        return None

def create_avatar_video(text, voice="en-US-JennyNeural"):
    encoded_key = st.session_state.did_key
    headers = {
        "Authorization": f"Basic {encoded_key}",
        "Content-Type": "application/json"
    }
    source_url = "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg"
    payload = {
        "script": {
            "type": "text",
            "provider": {"type": "microsoft", "voice_id": voice},
            "input": text
        },
        "source_url": source_url,
        "config": {"result_format": "mp4"}
    }
    
    try:
        with st.spinner("🎬 Creating avatar video..."):
            response = requests.post("https://api.d-id.com/talks", headers=headers, json=payload)
            response.raise_for_status()
            talk_data = response.json()
            talk_id = talk_data.get("id")
            
            if not talk_id:
                st.error("No talk ID received")
                return None
            
            progress_bar = st.progress(0)
            for i in range(30):
                time.sleep(1)
                progress_bar.progress((i + 1) / 30)
                status_response = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data.get("status") == "done":
                    progress_bar.empty()
                    return status_data.get("result_url")
                elif status_data.get("status") == "error":
                    progress_bar.empty()
                    st.error(f"Error: {status_data.get('error', {}).get('description', 'Unknown error')}")
                    return None
            
            progress_bar.empty()
            st.warning("Timeout waiting for video")
            return None
            
    except Exception as e:
        st.error(f"Error creating video: {e}")
        return None

VOICE_OPTIONS = {
    "Jenny (US Female)": "en-US-JennyNeural",
    "Guy (US Male)": "en-US-GuyNeural",
    "Aria (US Female)": "en-US-AriaNeural",
    "Sonia (UK Female)": "en-GB-SoniaNeural",
    "Ryan (UK Male)": "en-GB-RyanNeural"
}

with st.sidebar:
    st.header("⚙️ Settings")
    selected_voice_name = st.selectbox("Select Voice", options=list(VOICE_OPTIONS.keys()), index=0)
    selected_voice = VOICE_OPTIONS[selected_voice_name]
    auto_video = st.checkbox("Auto-create videos", value=True)
    st.divider()
    st.header("📹 Video History")
    if st.session_state.video_history:
        for video_url in reversed(st.session_state.video_history[-5:]):
            st.video(video_url)
    else:
        st.info("No videos created yet")
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

col1, col2 = st.columns([3, 2])

with col1:
    st.header("💬 Chat")
    
    if 'did_key' not in st.session_state:
        st.session_state.did_key = setup_did()
    
    agent = setup_agent()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "video_url" in message and message["video_url"]:
                st.video(message["video_url"])
    
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = agent.invoke({"input": prompt})
                    answer = response["output"]
                    st.markdown(answer)
                    
                    video_url = None
                    if auto_video:
                        video_url = create_avatar_video(answer, selected_voice)
                        if video_url:
                            st.video(video_url)
                            st.session_state.video_history.append(video_url)
                    
                    message_data = {"role": "assistant", "content": answer}
                    if video_url:
                        message_data["video_url"] = video_url
                    st.session_state.messages.append(message_data)
                    
                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    st.header("🎬 Video Preview")
    st.subheader("Create Custom Video")
    custom_text = st.text_area("Enter text for video", placeholder="Type something to create a custom video...", height=100)
    
    if st.button("🎥 Create Video", type="primary"):
        if custom_text:
            video_url = create_avatar_video(custom_text, selected_voice)
            if video_url:
                st.success("✅ Video created successfully!")
                st.video(video_url)
                st.session_state.video_history.append(video_url)
        else:
            st.warning("Please enter some text")
    
    st.divider()
    st.subheader("📊 Stats")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Messages", len(st.session_state.messages))
    with col_b:
        st.metric("Videos Created", len(st.session_state.video_history))

st.divider()
st.markdown("Built with ❤️ using LangChain, OpenAI, and D-ID")