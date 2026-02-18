# simple_test_no_langchain.py
import os
import base64
import requests
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("="*50)
print("🔍 TESTING YOUR SETUP (No LangChain)")
print("="*50)

# 1. Check if keys exist
openai_key = os.getenv("OPENAI_API_KEY")
serp_key = os.getenv("SERPAPI_API_KEY")
did_key = os.getenv("DID_API_KEY")

print(f"\n1️⃣ OPENAI API Key: {'✅ Found' if openai_key else '❌ Missing'}")
print(f"2️⃣ SERPAPI Key: {'✅ Found' if serp_key else '❌ Missing'}")
print(f"3️⃣ D-ID Key: {'✅ Found' if did_key else '❌ Missing'}")

# 2. Test OpenAI
print("\n🤖 Testing OpenAI...")
try:
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'Hello, I am working!' in 3 words"}],
        max_tokens=10
    )
    print(f"✅ OpenAI says: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI error: {e}")

# 3. Test SerpAPI directly (without LangChain)
print("\n🔍 Testing SerpAPI directly...")
try:
    params = {
        "q": "current time",
        "api_key": serp_key,
        "num": 1
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        print(f"✅ SerpAPI connection successful!")
        data = response.json()
        print(f"   Sample result: {str(data)[:100]}...")
    else:
        print(f"❌ SerpAPI error: {response.status_code}")
except Exception as e:
    print(f"❌ SerpAPI error: {e}")

# 4. Test D-ID
print("\n🎬 Testing D-ID connection...")
try:
    encoded = base64.b64encode(f"{did_key}:".encode()).decode()
    response = requests.get(
        "https://api.d-id.com/talks",
        headers={"Authorization": f"Basic {encoded}"}
    )
    if response.status_code == 200:
        print("✅ D-ID connection successful!")
    else:
        print(f"❌ D-ID error: {response.status_code}")
except Exception as e:
    print(f"❌ D-ID error: {e}")

print("\n" + "="*50)
print("✅ Basic test complete!")
print("="*50)