# 🔮 The Oracle - VintageLa AI Avatar Assistant

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2-green.svg)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT3.5-black.svg)](https://openai.com/)
[![D-ID](https://img.shields.io/badge/D-ID-Avatar-purple.svg)](https://www.d-id.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<div align="center">
  <img src="https://via.placeholder.com/800x400/5fa8a0/f5edd8?text=The+Oracle" alt="The Oracle Banner" width="800"/>
  <p><em>A mystical vintage-themed AI assistant that speaks through animated portraits</em></p>
</div>

## 📋 **Table of Contents**
- [Overview](#-overview)
- [Features](#-features)
- [Visual Design](#-visual-design)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [The Development Journey](#-the-development-journey)
- [Troubleshooting](#-troubleshooting)
- [Future Enhancements](#-future-enhancements)

## 🌟 **Overview**

**The Oracle** is not just another AI chatbot — it's a **vintage-themed mystical experience** that combines cutting-edge AI technology with an aesthetic that feels like discovering an ancient artifact in a dusty antique shop. Users can ask questions, receive wisdom from the Oracle, and watch as their answers are spoken by an animated vintage portrait.

The application seamlessly integrates:
- 🤖 **LangChain agents** for intelligent reasoning
- 🔍 **Google Search** for real-time information
- 🎬 **D-ID animated portraits** for visual engagement
- 🎨 **Custom vintage UI** for an immersive experience

## ✨ **Features**

### **Core Capabilities**
| Feature | Description |
|---------|-------------|
| **🔮 Intelligent Conversation** | Powered by GPT-3.5 with a custom "Oracle" persona |
| **🌐 Real-time Search** | Google integration via SerpAPI for current information |
| **🎭 Animated Portraits** | D-ID talking avatar videos from responses |
| **🗣️ Multiple Voices** | 5 distinct voice options (US/UK, Male/Female) |

### **Visual & UX Features**
- **🎨 Custom Vintage Design** - Hand-crafted CSS with sepia tones, bronze borders, and aged paper textures
- **📜 "Correspondence" Chat** - Styled like vintage letters with alternating bubble designs
- **🖼️ "Portrait Studio"** - Dedicated area for video previews and custom script creation
- **📊 Mystical Stats** - Track "Dispatches" and "Portraits" with vintage-styled metrics
- **📹 "Recent Portraits" Gallery** - Quick access to last 3 created videos

### **Technical Features**
- **💾 Session State** - Maintains conversation history
- **⚡ Cached Resources** - Optimized agent loading
- **🔄 Auto Video Generation** - Toggle on/off
- **🎥 Custom Video Creation** - Generate videos from any text
- **🧹 Chat Management** - Clear conversation with one click

## 🎨 **Visual Design**

The Oracle features a completely custom-designed interface:

### **Color Palette**
```
Primary Teal:    #5fa8a0 (background)
Header Teal:     #4a8880 (sidebar, header)
Vintage Paper:   #f5edd8 (chat bubbles, cards)
Antique Gold:    #d4a843 (accents, ribbon)
Bronze Border:   #a07840 (borders, shadows)
Dark Ink:        #2a1a08 (text)
```

### **Typography**
- **Playfair Display** - Elegant serif for headings
- **Josefin Sans** - Vintage sans-serif for labels
- **Special Elite** - Typewriter-style for chat text

### **Key Visual Elements**
- **Ribbon Badge** - Vintage-style title ribbon with shadow effects
- **Vintage Cards** - Raised panels with bronze borders and drop shadows
- **Custom Chat Bubbles** - Asymmetrical design with border variations
- **Pressed Buttons** - 3D effect with shadow offsets
- **Metric Displays** - Vintage-styled stat cards

## 🔄 **How It Works**

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│  ┌─────────────────┐  ┌────────────────────────────────────┐    │
│  │   SIDEBAR       │  │   MAIN CHAT AREA                   │    │
│  │  • Voice Select │  │  ┌─────────────────────────────┐  │    │
│  │  • Auto Video   │  │  │  User: "What's the weather?"│  │    │
│  │  • Recent Videos│  │  ├─────────────────────────────┤  │    │
│  │  • Clear Chat   │  │  │Oracle: *thinks, searches,   │  │    │
│  └─────────────────┘  │  │        responds with video* │  │    │
│                       │  └─────────────────────────────┘  │    │
│                       └────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AGENT PIPELINE                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │   User      │─▶│   Agent     │─▶│   Tool Decision     │     │
│  │   Question  │  │   Reasons   │  │   (Search or Answer)│     │
│  └─────────────┘  └─────────────┘  └───────────┬─────────┘     │
│                                                 │               │
│                          ┌──────────────────────┼───────────────┘
│                          ▼                      ▼
│  ┌─────────────────────┐  ┌───────────────────────────────────┐
│  │   Direct Answer     │  │   Google Search (SerpAPI)         │
│  │   from GPT-3.5      │  │   "weather in New York" → results │
│  └──────────┬──────────┘  └──────────────────┬────────────────┘
│             │                                 │
│             └───────────────┬─────────────────┘
│                             ▼
│  ┌─────────────────────────────────────────────────────────────┐
│  │                 Final Response Generation                    │
│  │         "The current weather in New York is 72°F..."        │
│  └───────────────────────────┬─────────────────────────────────┘
│                             ▼
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     VIDEO PIPELINE (Optional)                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  1. Text sent to D-ID API                                    │ │
│  │  2. Avatar video generated with selected voice              │ │
│  │  3. Video URL returned and displayed in chat                │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ **Technology Stack**

### **Core Technologies**
```
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Streamlit                          │  │
│  │              Web Framework & UI Components            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      AGENT LAYER                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   LangChain │  │   ReAct     │  │    Agent Executor   │  │
│  │   Framework │  │   Pattern   │  │    (langchain-classic)│  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │    OpenAI       │  │     SerpAPI     │  │    D-ID     │  │
│  │    GPT-3.5      │  │  Google Search  │  │   Avatar    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### **Detailed Stack**

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit 1.32 | Web UI framework |
| **Styling** | Custom CSS | Vintage aesthetic |
| **Agent Framework** | LangChain 1.2.10 | Agent orchestration |
| **Agent Runtime** | langchain-classic | AgentExecutor compatibility |
| **LLM** | OpenAI GPT-3.5 | Language understanding |
| **Search** | SerpAPI | Real-time web search |
| **Video** | D-ID API | Talking avatar generation |
| **Environment** | python-dotenv | API key management |

## 📦 **Installation**

### **Prerequisites**
- Python 3.13 or higher
- API keys for:
  - [OpenAI](https://platform.openai.com/api-keys)
  - [SerpAPI](https://serpapi.com/)
  - [D-ID](https://studio.d-id.com)

### **Step-by-Step Installation**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/the-oracle.git
cd the-oracle

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your API keys
echo "OPENAI_API_KEY=your-key-here" > .env
echo "SERPAPI_API_KEY=your-key-here" >> .env
echo "DID_API_KEY=your-key-here" >> .env

# 6. Run the application
streamlit run streamlit_app.py
```

### **requirements.txt**
```txt
langchain==1.2.10
langchain-community==0.4.1
langchain-core==1.2.13
langchain-openai==1.1.10
langchain-classic==1.0.1
openai==2.21.0
tiktoken==0.8.0
streamlit==1.32.0
python-dotenv==1.0.0
google-search-results==2.4.2
requests==2.31.0
```

## 📖 **Usage Guide**

### **Getting Started**

1. **Launch the app**: `streamlit run streamlit_app.py`
2. **Select a voice** from the sidebar dropdown
3. **Choose auto-video** option (on by default)
4. **Ask a question** in the chat input

### **Example Queries**

Try these questions to see the Oracle in action:

| Category | Example Query |
|----------|--------------|
| **Simple Q&A** | "What is the capital of France?" |
| **Current Info** | "What's the weather in Tokyo today?" |
| **News** | "Who won the latest Formula 1 race?" |
| **Jokes** | "Tell me a vintage-style joke" |
| **Philosophy** | "What is the meaning of life?" |
| **Custom Video** | Use "Custom Script" panel with any text |

### **Features Walkthrough**

#### **🔊 Voice Selection**
Choose from 5 voices in the sidebar:
- Jenny (US Female)
- Guy (US Male)
- Aria (US Female)
- Sonia (UK Female)
- Ryan (UK Male)

#### **🎬 Auto Video Generation**
- Toggle on/off in sidebar
- When on, every response generates an avatar video
- Videos appear in chat and are saved to history

#### **📹 Recent Portraits**
- Sidebar shows last 3 videos
- Click links to view full screen

#### **✍️ Custom Script**
- Enter any text in the Portrait Studio
- Click "Develop Portrait" to create a video
- Great for testing or standalone videos

#### **🗑️ Clear Correspondence**
- Reset conversation history
- Keeps first welcome message
- Video history also cleared

## 📁 **Project Structure**

```
the-oracle/
├── 📄 streamlit_app.py          # Main application
├── 📄 simple_agent_fixed.py      # Basic agent test
├── 📄 simple_test.py              # API key tester
├── 📓 1 - LangChain Agents - agent.ipynb  # Development notebook
├── 📄 .env                        # API keys (not in repo)
├── 📄 requirements.txt            # Dependencies
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📁 .venv/                       # Virtual environment
└── 📁 assets/                       # Images, screenshots
```

## 🚀 **The Development Journey**

This project represents a journey from concept to completion, overcoming several technical challenges:

### **Phase 1: Foundation**
- ✅ Set up Python 3.13 virtual environment
- ✅ Obtained API keys (OpenAI, SerpAPI, D-ID)
- ✅ Created basic API test scripts

### **Phase 2: LangChain Integration**
- ✅ Built simple agent with search capability
- 🔥 **Challenge**: Import errors with LangChain 1.0+
- ✅ **Solution**: Used `langchain_core` imports and `langchain-classic`

### **Phase 3: Python 3.13 Compatibility**
- 🔥 **Challenge**: `tiktoken` required Rust compiler
- ✅ **Solution**: Installed `tiktoken==0.8.0` with pre-built wheels

### **Phase 4: D-ID Integration**
- ✅ Created avatar video generation function
- ✅ Added polling mechanism for video completion
- ✅ Integrated with agent responses

### **Phase 5: Streamlit UI**
- ✅ Built two-column layout
- ✅ Designed custom vintage CSS theme
- ✅ Added session state management
- ✅ Created video history tracking

### **Phase 6: Polish & Refinement**
- ✅ Added voice selection
- ✅ Created custom video panel
- ✅ Implemented stats tracking
- ✅ Added clear chat functionality
- ✅ Optimized with caching

## 🐛 **Troubleshooting**

### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **ImportError: cannot import name 'Tool'** | Use `from langchain_core.tools import Tool` |
| **ImportError: cannot import name 'AgentExecutor'** | Install `langchain-classic` and import from there |
| **tiktoken installation fails** | Install `tiktoken==0.8.0` (Python 3.13 compatible) |
| **D-ID video not generating** | Check API key format; ensure base64 encoding |
| **Agent not searching** | Verify SerpAPI key; check prompt format |
| **Streamlit not found** | Activate virtual environment first |

### **Debug Commands**

```bash
# Test API keys
python simple_test.py

# Test basic agent
python simple_agent_fixed.py

# Check installed packages
pip list | findstr langchain

# Run with debug logging
streamlit run streamlit_app.py --logger.level=debug
```

## 🔮 **Future Enhancements**

### **Short-term Improvements**
- [ ] Add custom avatar image upload
- [ ] Implement conversation export
- [ ] Add more voice options
- [ ] Create shareable video links

### **Long-term Vision**
- [ ] Multi-language support
- [ ] User authentication system
- [ ] Database storage for conversations
- [ ] Mobile app version
- [ ] Custom Oracle persona training

## 🤝 **Contributing**

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- [LangChain](https://langchain.com/) for the incredible agent framework
- [OpenAI](https://openai.com/) for GPT-3.5
- [D-ID](https://www.d-id.com/) for avatar technology
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [SerpAPI](https://serpapi.com/) for search capabilities
- All the open-source packages that made this possible

## 📧 **Contact**





---

