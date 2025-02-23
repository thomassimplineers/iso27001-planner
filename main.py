import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda miljövariabler från .env filen
load_dotenv()

# Konfigurera Gemini API med din API-nyckel
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Välj Gemini Pro-modellen
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(prompt):
    """Skicka en förfrågan till Gemini API och få ett svar"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Ett fel uppstod: {str(e)}"

def main():
    print("Välkommen till Gemini API Test App!")
    print("Skriv 'avsluta' för att avsluta programmet.")
    
    while True:
        user_input = input("\nSkriv din fråga: ")
        
        if user_input.lower() == 'avsluta':
            print("Avslutar programmet...")
            break
            
        response = get_gemini_response(user_input)
        print("\nGemini svarar:", response)

if __name__ == "__main__":
    if not GOOGLE_API_KEY:
        print("Varning: Ingen API-nyckel hittades. Skapa en .env fil med din GOOGLE_API_KEY.")
    else:
        main()
