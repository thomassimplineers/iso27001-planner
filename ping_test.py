import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda miljövariabler
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def test_api_connection():
    try:
        # Skapa en modell-instans
        model = genai.GenerativeModel('gemini-pro')
        
        # Skicka ett ping-meddelande
        response = model.generate_content('Ping test: Svara "OK" om du får detta meddelande.')
        
        # Skriv ut svaret
        print("\n✅ API-anslutning lyckades!")
        print(f"Svar från API: {response.text}\n")
        
    except Exception as e:
        print(f"\n❌ Kunde inte ansluta till API:et.")
        print(f"Felmeddelande: {str(e)}\n")

if __name__ == "__main__":
    test_api_connection()
