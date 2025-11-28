import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
print(f"API Key present: {bool(api_key)}")

if api_key:
    try:
        print("Importing langchain_google_genai...")
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        print("Initializing ChatGoogleGenerativeAI...")
        llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", google_api_key=api_key)
        
        print("Invoking LLM with 'Hello'...")
        start = time.time()
        response = llm.invoke("Hello, are you working?")
        end = time.time()
        
        print(f"Response received in {end - start:.2f} seconds.")
        print(f"Response: {response.content}")
        
    except Exception as e:
        print(f"LLM Test Failed: {e}")
else:
    print("No API Key found.")
