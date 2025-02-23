# ISO 27001 Certifieringsplanerare

En interaktiv webbapplikation för att planera och genomföra ISO 27001-certifiering med AI-stöd.

## Funktioner

- Steg-för-steg implementeringsguide
- AI-driven analys och rekommendationer
- Interaktiv checklista
- Handlingsplan med aktivitetshantering
- Automatisk sparning av framsteg
- Framstegsindikator för implementationen

## Installation

1. Klona repositoryt:
```bash
git clone <repository-url>
cd gemini-test-app
```

2. Skapa en virtuell miljö:
```bash
python -m venv venv
source venv/bin/activate  # På macOS/Linux
# eller
.\venv\Scripts\activate  # På Windows
```

3. Installera dependencies:
```bash
pip install -r requirements.txt
```

4. Skapa en `.env` fil och lägg till din Gemini API-nyckel:
```
GOOGLE_API_KEY=din_api_nyckel_här
```

För att få en API-nyckel:
1. Gå till [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Skapa ett nytt projekt eller välj ett befintligt
3. Generera en ny API-nyckel
4. Kopiera nyckeln till din `.env` fil

## Starta applikationen

1. Aktivera den virtuella miljön om den inte redan är aktiverad:
```bash
source venv/bin/activate  # På macOS/Linux
# eller
.\venv\Scripts\activate  # På Windows
```

2. Starta applikationen:
```bash
streamlit run iso27001_planner.py
```

Applikationen öppnas automatiskt i din standardwebbläsare på `http://localhost:8501`

## Användning

1. **Implementeringsguide**: Börja med att gå igenom implementeringsguiden för att få en överblick över processen
2. **Organisationsinformation**: Fyll i grundläggande information om din organisation
3. **Checklista**: Använd checklistan för att hålla koll på viktiga milstolpar
4. **Handlingsplan**: Skapa och hantera specifika aktiviteter
5. **AI-stöd**: Använd AI-knapparna för att få specifika rekommendationer i varje steg

## Data och Sparning

- All data sparas automatiskt i en lokal fil (`iso27001_data.json`)
- Du kan när som helst exportera din data via "Exportera Data"-sektionen
- Varje sektion har en egen "Spara"-knapp för manuell sparning

## Support

Om du stöter på problem eller har frågor:
1. Kontrollera att alla dependencies är korrekt installerade
2. Verifiera att din `.env` fil är korrekt konfigurerad
3. Kontrollera att du har en aktiv internetanslutning (krävs för AI-funktionerna)

## Bidra

Känner du till förbättringar eller har förslag? Skapa gärna en Issue eller Pull Request!
