try:
    from langchain.memory import ConversationBufferMemory
    print("✅ Found ConversationBufferMemory in langchain.memory")
except ImportError:
    print("❌ Not found in langchain.memory")
    try:
        from langchain_core.memory import ConversationBufferMemory
        print("✅ Found ConversationBufferMemory in langchain_core.memory")
    except ImportError:
        print("❌ Not found in langchain_core.memory")

try:
    import notebook
    print("✅ Jupyter notebook is installed")
except ImportError:
    print("❌ Jupyter notebook is NOT installed")
