import json
import time
import google.generativeai as genai

# --- Configure Gemini API ---
API_KEY = "AIzaSyAI5qePEY4cVNt8jUDDUrtUv-SVjDKlQ9E"   # 🔑 Replace with your Gemini API key
genai.configure(api_key=API_KEY)
MODEL = "gemini-1.5-flash"

def generate_gemini_response(prompt: str):
    """Send prompt to Gemini and return text output."""
    for i in range(5):  # retry up to 5 times
        try:
            response = genai.GenerativeModel(MODEL).generate_content(prompt)
            if response.text:
                return response.text.strip()
        except Exception as e:
            wait_time = 2 ** i
            print(f"⚠️ API error: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
    return "⚠️ Sorry, Gemini API failed after several attempts."

