import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {api_key[:10]}..." if api_key else "No API key found!")

try:
    genai.configure(api_key=api_key)
        print("\n📋 Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✅ {model.name}")
    
    # Test with correct model name
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("\n✅ Gemini working!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")