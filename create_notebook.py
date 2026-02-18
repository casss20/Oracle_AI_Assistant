import json
import os

notebook_path = r"c:\Users\casse\OneDrive\Documents\GitHub\Openai_langchain\1 - LangChain Agents - agent.ipynb"

cells = []

# Cell 1: Install
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Install packages if needed (commented out as they are in .venv)\n",
        "# !pip install langchain-openai langchain-community langchain-classic langchain-core python-dotenv google-search-results openai requests notebook ipykernel tiktoken"
    ]
})

# Cell 2: Imports
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import os\n",
        "import base64\n",
        "import time\n",
        "import requests\n",
        "from dotenv import load_dotenv\n",
        "from openai import OpenAI\n",
        "\n",
        "# LangChain imports - updated for your environment\n",
        "from langchain_openai import ChatOpenAI\n",
        "from langchain_classic.agents import AgentExecutor, create_react_agent\n",
        "from langchain_classic.memory import ConversationBufferMemory\n",
        "from langchain_core.tools import Tool\n",
        "from langchain_core.prompts import PromptTemplate\n",
        "from langchain_community.utilities import SerpAPIWrapper\n",
        "\n",
        "print(\"✅ All imports successful!\")\n",
        "print(f\"✅ OpenAI import: {ChatOpenAI}\")"
    ]
})

# Cell 3: Load Env
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Load .env file\n",
        "load_dotenv()\n",
        "\n",
        "# Check if keys are loaded\n",
        "OPENAI_API_KEY = os.getenv(\"OPENAI_API_KEY\")\n",
        "SERPAPI_API_KEY = os.getenv(\"SERPAPI_API_KEY\")\n",
        "DID_API_KEY = os.getenv(\"DID_API_KEY\")\n",
        "\n",
        "print(f\"OPENAI_API_KEY: {'✅ Found' if OPENAI_API_KEY else '❌ Missing'}\")\n",
        "print(f\"SERPAPI_API_KEY: {'✅ Found' if SERPAPI_API_KEY else '❌ Missing'}\")\n",
        "print(f\"DID_API_KEY: {'✅ Found' if DID_API_KEY else '❌ Missing'}\")\n",
        "\n",
        "if not all([OPENAI_API_KEY, SERPAPI_API_KEY, DID_API_KEY]):\n",
        "    print(\"⚠️  Warning: Some API keys are missing. Check your .env file!\")"
    ]
})

# Cell 4: Setup Components
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Initialize LangChain LLM\n",
        "llm = ChatOpenAI(\n",
        "    api_key=OPENAI_API_KEY,\n",
        "    model=\"gpt-3.5-turbo\",  # Using 3.5 for speed\n",
        "    temperature=0\n",
        ")\n",
        "\n",
        "# Initialize SerpAPI for search\n",
        "search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)\n",
        "\n",
        "print(\"✅ LLM and Search initialized\")"
    ]
})

# Cell 5: Create Search Tool
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create search tool\n",
        "search_tool = Tool(\n",
        "    name=\"Google Search\",\n",
        "    func=search.run,\n",
        "    description=\"Useful for searching current information from Google. Input should be a search query.\"\n",
        ")\n",
        "\n",
        "tools = [search_tool]\n",
        "print(f\"✅ Created tool: {tools[0].name}\")"
    ]
})

# Cell 6: Test Basic Agent
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create a simple prompt\n",
        "prompt = PromptTemplate.from_template(\"\"\"\n",
        "Answer the following question using the search tool if needed.\n",
        "\n",
        "Question: {input}\n",
        "{agent_scratchpad}\n",
        "\"\"\")\n",
        "\n",
        "# Create agent\n",
        "agent = create_react_agent(llm, tools, prompt)\n",
        "\n",
        "# Create executor\n",
        "agent_executor = AgentExecutor(\n",
        "    agent=agent,\n",
        "    tools=tools,\n",
        "    verbose=True,\n",
        "    handle_parsing_errors=True  # Added for robustness\n",
        ")\n",
        "\n",
        "# Test it\n",
        "print(\"🔍 Testing agent with a simple question...\")\n",
        "result = agent_executor.invoke({\"input\": \"What is 2+2?\"})\n",
        "print(f\"\\n📝 Answer: {result['output']}\")"
    ]
})

# Cell 7: Add Memory
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create memory for conversation history\n",
        "memory = ConversationBufferMemory(\n",
        "    memory_key=\"chat_history\",\n",
        "    return_messages=True\n",
        ")\n",
        "\n",
        "# Create agent with memory\n",
        "agent_with_memory = create_react_agent(llm, tools, prompt)\n",
        "executor_with_memory = AgentExecutor(\n",
        "    agent=agent_with_memory,\n",
        "    tools=tools,\n",
        "    memory=memory,\n",
        "    verbose=True,\n",
        "    handle_parsing_errors=True\n",
        ")\n",
        "\n",
        "print(\"✅ Agent with memory created\")\n",
        "\n",
        "# Test conversation\n",
        "print(\"\\n🗣️ Testing conversation...\")\n",
        "result1 = executor_with_memory.invoke({\"input\": \"My name is John\"})\n",
        "print(f\"Response 1: {result1['output']}\")\n",
        "\n",
        "result2 = executor_with_memory.invoke({\"input\": \"What's my name?\"})\n",
        "print(f\"Response 2: {result2['output']}\")"
    ]
})

# Cell 8: Add D-ID Avatar
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# D-ID setup\n",
        "encoded_did_key = base64.b64encode(f\"{DID_API_KEY}:\".encode()).decode()\n",
        "DID_API_URL = \"https://api.d-id.com/talks\"\n",
        "\n",
        "def create_avatar_video(text, source_url=\"https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg\"):\n",
        "    \"\"\"Create a talking avatar video from text\"\"\"\n",
        "    \n",
        "    headers = {\n",
        "        \"Authorization\": f\"Basic {encoded_did_key}\",\n",
        "        \"Content-Type\": \"application/json\"\n",
        "    }\n",
        "    \n",
        "    payload = {\n",
        "        \"script\": {\n",
        "            \"type\": \"text\",\n",
        "            \"provider\": {\"type\": \"microsoft\", \"voice_id\": \"en-US-JennyNeural\"},\n",
        "            \"input\": text\n",
        "        },\n",
        "        \"source_url\": source_url\n",
        "    }\n",
        "    \n",
        "    try:\n",
        "        print(\"🎬 Creating avatar video...\")\n",
        "        response = requests.post(DID_API_URL, headers=headers, json=payload)\n",
        "        response.raise_for_status()\n",
        "        talk_data = response.json()\n",
        "        talk_id = talk_data.get(\"id\")\n",
        "        \n",
        "        if not talk_id:\n",
        "            return None, \"No talk ID received\"\n",
        "        \n",
        "        print(\"⏳ Waiting for video to render...\")\n",
        "        for attempt in range(30):\n",
        "            status_response = requests.get(f\"{DID_API_URL}/{talk_id}\", headers=headers)\n",
        "            status_response.raise_for_status()\n",
        "            status_data = status_response.json()\n",
        "            \n",
        "            if status_data.get(\"status\") == \"done\":\n",
        "                video_url = status_data.get(\"result_url\")\n",
        "                print(f\"✅ Video ready!\")\n",
        "                return video_url, None\n",
        "            elif status_data.get(\"status\") == \"error\":\n",
        "                error_msg = status_data.get('error', {}).get('description', 'Unknown error')\n",
        "                return None, error_msg\n",
        "            \n",
        "            time.sleep(1)\n",
        "        \n",
        "        return None, \"Timeout waiting for video\"\n",
        "        \n",
        "    except Exception as e:\n",
        "        return None, str(e)\n",
        "\n",
        "# Test D-ID with a simple message\n",
        "print(\"🎬 Testing D-ID connection...\")\n",
        "video_url, error = create_avatar_video(\"Hello, I am your AI assistant!\")\n",
        "if video_url:\n",
        "    print(f\"✅ Success! Video URL: {video_url}\")\n",
        "else:\n",
        "    print(f\"❌ Error: {error}\")"
    ]
})

# Cell 9: Create Avatar Tool
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "def avatar_tool_function(text):\n",
        "    \"\"\"Wrapper function for LangChain tool\"\"\"\n",
        "    video_url, error = create_avatar_video(text)\n",
        "    if video_url:\n",
        "        return f\"✅ Successfully created avatar video. You can view it at: {video_url}\"\n",
        "    else:\n",
        "        return f\"❌ Failed to create avatar video: {error}\"\n",
        "\n",
        "# Create avatar tool\n",
        "avatar_tool = Tool(\n",
        "    name=\"Avatar Creator\",\n",
        "    func=avatar_tool_function,\n",
        "    description=\"Creates a talking avatar video from text. Use this when you need to create a video of an avatar speaking.\"\n",
        ")\n",
        "\n",
        "# Add to tools\n",
        "all_tools = [search_tool, avatar_tool]\n",
        "print(f\"✅ Created {len(all_tools)} tools: {[tool.name for tool in all_tools]}\")"
    ]
})

# Cell 10: Full Agent
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create prompt template with tool names\n",
        "full_prompt = PromptTemplate.from_template(\"\"\"\n",
        "You are a helpful AI assistant with access to the following tools:\n",
        "\n",
        "{tools}\n",
        "\n",
        "Use the following format:\n",
        "\n",
        "Question: the input question\n",
        "Thought: think about what to do\n",
        "Action: the action to take [{tool_names}]\n",
        "Action Input: input for the action\n",
        "Observation: result of the action\n",
        "... (repeat as needed)\n",
        "Thought: I now know the answer\n",
        "Final Answer: final response\n",
        "\n",
        "Question: {input}\n",
        "{agent_scratchpad}\n",
        "\"\"\")\n",
        "\n",
        "# Create agent with both tools\n",
        "full_agent = create_react_agent(llm, all_tools, full_prompt)\n",
        "\n",
        "# Create fresh memory\n",
        "full_memory = ConversationBufferMemory(\n",
        "    memory_key=\"chat_history\",\n",
        "    return_messages=True\n",
        ")\n",
        "\n",
        "full_executor = AgentExecutor(\n",
        "    agent=full_agent,\n",
        "    tools=all_tools,\n",
        "    memory=full_memory,\n",
        "    verbose=True,\n",
        "    handle_parsing_errors=True,\n",
        "    max_iterations=3\n",
        ")\n",
        "\n",
        "print(\"✅ Full agent with avatar and search ready!\")"
    ]
})

# Cell 11: Test Full Agent
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Test with a question that might use both tools\n",
        "test_question = \"What is the current weather in New York and create a video about it?\"\n",
        "\n",
        "print(f\"🔍 Testing full agent with: {test_question}\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "result = full_executor.invoke({\"input\": test_question})\n",
        "\n",
        "print(\"=\"*60)\n",
        "print(f\"📝 Final Answer: {result['output']}\")"
    ]
})

# Cell 12: Interactive Chat
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "def chat_with_agent():\n",
        "    \"\"\"Interactive chat with the agent\"\"\"\n",
        "    print(\"🤖 Agent is ready! Type 'quit' to exit.\")\n",
        "    print(\"-\"*40)\n",
        "    \n",
        "    while True:\n",
        "        user_input = input(\"\\nYou: \")\n",
        "        if user_input.lower() in ['quit', 'exit', 'q']:\n",
        "            print(\"Goodbye! 👋\")\n",
        "            break\n",
        "        \n",
        "        print(\"\\n🤔 Thinking...\")\n",
        "        result = full_executor.invoke({\"input\": user_input})\n",
        "        print(f\"\\nAgent: {result['output']}\")\n",
        "\n",
        "# Uncomment to run interactive chat\n",
        "# chat_with_agent()"
    ]
})

# Cell 13: Save Conversation
cells.append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import json\n",
        "from datetime import datetime\n",
        "\n",
        "def save_conversation():\n",
        "    \"\"\"Save conversation history to a file\"\"\"\n",
        "    # Check if chat_memory exists (ConversationBufferMemory has chat_memory)\n",
        "    if hasattr(full_executor.memory, 'chat_memory'):\n",
        "        messages = full_executor.memory.chat_memory.messages\n",
        "        conversation = []\n",
        "        \n",
        "        for msg in messages:\n",
        "            conversation.append({\n",
        "                \"role\": msg.type,\n",
        "                \"content\": msg.content,\n",
        "                \"timestamp\": datetime.now().isoformat()\n",
        "            })\n",
        "        \n",
        "        filename = f\"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json\"\n",
        "        with open(filename, 'w') as f:\n",
        "            json.dump(conversation, f, indent=2)\n",
        "        \n",
        "        print(f\"✅ Conversation saved to {filename}\")\n",
        "        return filename\n",
        "    else:\n",
        "        print(\"❌ No conversation to save\")\n",
        "        return None\n",
        "\n",
        "# Save the conversation\n",
        "save_conversation()"
    ]
})

notebook_content = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=1)

print(f"✅ Recreated notebook at {notebook_path}")
