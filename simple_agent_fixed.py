# simple_agent_fixed.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

load_dotenv()

print("="*50)
print("🤖 SIMPLE LANGCHAIN AGENT")
print("Type 'quit' or 'exit' to stop")
print("="*50)

try:
    # 1. Setup LLM
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0
    )
    print("✅ LLM created")

    # 2. Setup search
    search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
    print("✅ Search wrapper created")

    # 3. Create tools
    tools = [
        Tool(
            name="Google Search",
            func=search.run,
            description="Search Google for current information"
        )
    ]
    print("✅ Tools created")

    # 4. Create prompt
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
    print("✅ Prompt created")

    # 5. Create agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True
    )
    print("✅ Agent created\n")

    # 6. Interactive loop
    while True:
        user_input = input("🔍 You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break
        
        try:
            print("\n⏳ Thinking...\n")
            result = agent_executor.invoke({"input": user_input})
            print(f"🤖 Agent: {result['output']}\n")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error on this question: {e}\n")

except Exception as e:
    print(f"❌ Setup Error: {e}")
    import traceback
    traceback.print_exc()