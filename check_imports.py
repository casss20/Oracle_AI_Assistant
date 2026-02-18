try:
    from langchain.agents import AgentExecutor, create_react_agent
    print("✅ Successfully imported AgentExecutor, create_react_agent from langchain.agents")
except ImportError as e:
    print(f"❌ Failed to import from langchain.agents: {e}")
    try:
        from langchain.agents.agent import AgentExecutor
        print("✅ Found AgentExecutor in langchain.agents.agent")
    except ImportError:
        print("❌ Could not find AgentExecutor")
        
    try:
        from langchain.agents.react.agent import create_react_agent
        print("✅ Found create_react_agent in langchain.agents.react.agent")
    except ImportError:
        print("❌ Could not find create_react_agent")
