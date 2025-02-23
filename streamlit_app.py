import streamlit as st
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Konfigurera sidan
st.set_page_config(
    page_title="ISO 27001 Certifieringsplanering",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .stCheckbox {
            font-size: 1.1rem;
        }
        .main {
            padding: 2rem;
        }
        h1 {
            color: #2c3e50;
        }
        .stAlert {
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Huvudtitel
st.title("📋 ISO 27001 Certifieringsplanering")
st.markdown("---")

# Funktioner för datahantering
def save_data_to_file():
    """Spara data till JSON-fil"""
    try:
        with open('iso27001_data.json', 'w', encoding='utf-8') as f:
            json.dump(st.session_state.iso_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Kunde inte spara data: {str(e)}")
        return False

def load_data_from_file():
    """Ladda data från JSON-fil"""
    try:
        if os.path.exists('iso27001_data.json'):
            with open('iso27001_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Kunde inte ladda data: {str(e)}")
    return {
        'organisation_info': {},
        'checklists': {
            'ledningens_engagemang': {},
            'scope': {},
            'riskanalys': {},
            'policyer': {},
            'kontroller': {}
        }
    }

# Initiera session state för att spara data
if 'iso_data' not in st.session_state:
    st.session_state.iso_data = load_data_from_file()

# Konfigurera Gemini
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Fallback för lokal utveckling

if not GOOGLE_API_KEY:
    st.error("❌ Ingen API-nyckel hittad. Kontakta administratören.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_ai_analysis(data):
    """Få AI-analys från Gemini"""
    try:
        # Skapa en strukturerad prompt för analys
        prompt = f"""
        Analysera följande ISO 27001-implementeringsdata och ge konkreta rekommendationer:

        Organisationsinformation:
        - Namn: {data['organisation_info'].get('org_name', 'Ej angivet')}
        - Antal anställda: {data['organisation_info'].get('org_size', 'Ej angivet')}
        
        Checklista status:
        Ledningens engagemang:
        {', '.join([k for k, v in data['checklists']['ledningens_engagemang'].items() if v])}
        
        Scope:
        {', '.join([k for k, v in data['checklists']['scope'].items() if v])}
        
        Riskanalys:
        {', '.join([k for k, v in data['checklists']['riskanalys'].items() if v])}
        
        Ge specifika rekommendationer för:
        1. Nästa kritiska steg
        2. Potentiella risker att vara uppmärksam på
        3. Förslag på förbättringar
        4. Tidslinje för implementation
        
        Svara på svenska och var konkret i dina rekommendationer.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Kunde inte generera AI-analys: {str(e)}"

# Sidopanel för navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Välj sektion:",
        ["Implementeringsguide", "Organisationsinformation", "Checklista", "Handlingsplan", "Exportera Data"]
    )

# Implementeringsguide
if page == "Implementeringsguide":
    st.header("🗺️ ISO 27001 Implementeringsguide")
    
    # Definiera implementeringsstegen
    implementation_steps = {
        "1. Samla ditt team": {
            "description": """
            - Identifiera nyckelpersoner från olika avdelningar (IT, HR, juridik, kvalitet)
            - Definiera roller och ansvar
            - Skapa en RACI-matris
            """,
            "estimated_time": "1 vecka",
            "deliverables": "Projekt RACI-matris, utkast till Statement of Applicability och Scope"
        },
        "2. Gap-analys": {
            "description": """
            - Utvärdera nuvarande säkerhetsstatus
            - Identifiera gap mot ISO 27001-standarden
            - Dokumentera resultat och rekommendationer
            """,
            "estimated_time": "2 veckor",
            "deliverables": "Gap-analysrapport med identifierade risker och brister"
        },
        "3. Prioritera åtgärder": {
            "description": """
            - Analysera gap-analysens resultat
            - Prioritera åtgärder baserat på risk och resurser
            - Skapa handlingsplan
            """,
            "estimated_time": "6 veckor",
            "deliverables": "Prioriterad åtgärdsplan med tidslinjer"
        },
        "4. Tillgångshantering": {
            "description": """
            - Identifiera informationstillgångar
            - Klassificera tillgångar efter känslighet
            - Upprätta tillgångsregister
            """,
            "estimated_time": "2 veckor",
            "deliverables": "Uppdaterat tillgångsregister"
        },
        "5. Riskhantering": {
            "description": """
            - Genomför riskbedömning
            - Identifiera och värdera hot
            - Utveckla riskreducerande åtgärder
            """,
            "estimated_time": "2 veckor",
            "deliverables": "Riskbedömning och åtgärdsplan"
        },
        "6. ISMS-dokumentation": {
            "description": """
            - Utveckla policyer och procedurer
            - Skapa rutiner och arbetsinstruktioner
            - Dokumentera säkerhetskontroller
            """,
            "estimated_time": "6 veckor",
            "deliverables": "Komplett ISMS-dokumentation"
        },
        "7. Intern revision": {
            "description": """
            - Planera intern revision
            - Genomför revision av ISMS
            - Dokumentera resultat och avvikelser
            """,
            "estimated_time": "2 veckor",
            "deliverables": "Intern revisionsrapport"
        },
        "8. Ledningens genomgång": {
            "description": """
            - Presentera resultat för ledningen
            - Utvärdera ISMS effektivitet
            - Besluta om förbättringsåtgärder
            """,
            "estimated_time": "2 veckor",
            "deliverables": "Protokoll från ledningens genomgång"
        },
        "9. Extern revision och certifiering": {
            "description": """
            - Välj certifieringsorgan
            - Genomgå steg 1-revision
            - Genomgå steg 2-revision (platsbesök)
            """,
            "estimated_time": "2 veckor",
            "deliverables": "ISO 27001-certifiering"
        }
    }
    
    # Beräkna total progress
    if 'step_progress' not in st.session_state.iso_data:
        st.session_state.iso_data['step_progress'] = {}
    
    total_steps = len(implementation_steps)
    completed_steps = sum(st.session_state.iso_data['step_progress'].values())
    
    # Visa total progress
    st.progress(completed_steps / total_steps)
    st.write(f"Total framsteg: {int((completed_steps / total_steps) * 100)}%")
    
    # Visa varje steg med detaljer
    for step, details in implementation_steps.items():
        with st.expander(f"{step} ({details['estimated_time']})"):
            # Visa beskrivning och leverabler
            st.markdown(details['description'])
            st.markdown(f"**Leverabler:** {details['deliverables']}")
            
            # Checkbox för att markera steget som klart
            step_key = step.split('.')[0]  # Använd endast numret som nyckel
            is_complete = st.checkbox(
                "Markera som klar",
                key=f"step_{step_key}",
                value=st.session_state.iso_data['step_progress'].get(step_key, False)
            )
            st.session_state.iso_data['step_progress'][step_key] = is_complete
            
            # Visa AI-rekommendationer för detta steg
            if st.button(f"🤖 Få AI-rekommendationer för {step}", key=f"ai_{step_key}"):
                with st.spinner("Analyserar och genererar rekommendationer..."):
                    prompt = f"""
                    Ge konkreta rekommendationer för följande steg i ISO 27001-implementationen:
                    
                    Steg: {step}
                    Beskrivning: {details['description']}
                    Förväntade leverabler: {details['deliverables']}
                    
                    Ge specifika, praktiska råd om:
                    1. Hur man bäst genomför detta steg
                    2. Vanliga fallgropar att undvika
                    3. Viktiga framgångsfaktorer
                    4. Konkreta exempel på best practices
                    
                    Svara på svenska och var mycket specifik.
                    """
                    response = model.generate_content(prompt)
                    st.markdown("### AI-rekommendationer")
                    st.markdown(response.text)
    
    # Spara-knapp för framsteg
    if st.button("💾 Spara framsteg"):
        if save_data_to_file():
            st.success("Framsteg sparade!")

# Organisationsinformation
elif page == "Organisationsinformation":
    st.header("🏢 Organisationsinformation")
    
    col1, col2 = st.columns(2)
    with col1:
        org_name = st.text_input("Organisationens namn", 
                                st.session_state.iso_data['organisation_info'].get('org_name', ''))
        org_size = st.number_input("Antal anställda", 
                                 min_value=1, 
                                 value=st.session_state.iso_data['organisation_info'].get('org_size', 1))
    with col2:
        contact_person = st.text_input("Kontaktperson", 
                                     st.session_state.iso_data['organisation_info'].get('contact_person', ''))
        target_date = st.date_input("Målsättning för certifiering", 
                                  value=datetime.strptime(st.session_state.iso_data['organisation_info'].get('target_date', datetime.today().strftime('%Y-%m-%d')), '%Y-%m-%d'))
    
    st.session_state.iso_data['organisation_info'].update({
        'org_name': org_name,
        'org_size': org_size,
        'contact_person': contact_person,
        'target_date': target_date.strftime('%Y-%m-%d')
    })
    
    # Spara-knapp
    if st.button("💾 Spara ändringar"):
        if save_data_to_file():
            st.success("Data sparad!")

# Checklista
elif page == "Checklista":
    st.header("✅ Checklista för ISO 27001")
    
    # Ledningens engagemang
    st.subheader("1. Ledningens engagemang")
    changed = False
    
    engagement_values = {
        'ledning_godkant': st.checkbox("Ledningen har godkänt ISO 27001-projektet", 
                                     st.session_state.iso_data['checklists']['ledningens_engagemang'].get('ledning_godkant', False)),
        'resurser_allokerade': st.checkbox("Nödvändiga resurser har allokerats", 
                                         st.session_state.iso_data['checklists']['ledningens_engagemang'].get('resurser_allokerade', False)),
        'projektledare_utsedd': st.checkbox("Projektledare har utsetts", 
                                          st.session_state.iso_data['checklists']['ledningens_engagemang'].get('projektledare_utsedd', False))
    }
    
    if engagement_values != st.session_state.iso_data['checklists']['ledningens_engagemang']:
        changed = True
        st.session_state.iso_data['checklists']['ledningens_engagemang'] = engagement_values

    # Omfattning (Scope)
    st.subheader("2. Omfattning (Scope)")
    st.session_state.iso_data['checklists']['scope'].update({
        'scope_definierat': st.checkbox("Omfattningen av ISMS är definierad", 
                                      st.session_state.iso_data['checklists']['scope'].get('scope_definierat', False)),
        'granser_dokumenterade': st.checkbox("Organisatoriska gränser är dokumenterade", 
                                           st.session_state.iso_data['checklists']['scope'].get('granser_dokumenterade', False)),
        'undantag_dokumenterade': st.checkbox("Eventuella undantag är dokumenterade och motiverade", 
                                            st.session_state.iso_data['checklists']['scope'].get('undantag_dokumenterade', False))
    })
    
    # Riskanalys
    st.subheader("3. Riskanalys")
    st.session_state.iso_data['checklists']['riskanalys'].update({
        'metodik_vald': st.checkbox("Riskanalysmetodik är vald", 
                                  st.session_state.iso_data['checklists']['riskanalys'].get('metodik_vald', False)),
        'tillgangar_identifierade': st.checkbox("Informationstillgångar är identifierade", 
                                              st.session_state.iso_data['checklists']['riskanalys'].get('tillgangar_identifierade', False)),
        'risker_varderade': st.checkbox("Risker är värderade", 
                                      st.session_state.iso_data['checklists']['riskanalys'].get('risker_varderade', False))
    })

    # Spara-knapp för checklistan
    if changed:
        if st.button("💾 Spara ändringar"):
            if save_data_to_file():
                st.success("Checklista sparad!")

# Handlingsplan
elif page == "Handlingsplan":
    st.header("📝 Handlingsplan")
    
    # AI-analys av handlingsplan
    if st.button("🤖 Få AI-analys av handlingsplan"):
        with st.spinner("Analyserar handlingsplan och genererar rekommendationer..."):
            activities = st.session_state.iso_data.get('activities', [])
            org_info = st.session_state.iso_data.get('organisation_info', {})
            checklists = st.session_state.iso_data.get('checklists', {})
            
            prompt = f"""
            Analysera följande handlingsplan för ISO 27001-implementering och ge konkreta rekommendationer:

            Organisationsinformation:
            - Namn: {org_info.get('org_name', 'Ej angivet')}
            - Antal anställda: {org_info.get('org_size', 'Ej angivet')}
            - Målsättning för certifiering: {org_info.get('target_date', 'Ej angivet')}

            Nuvarande aktiviteter i handlingsplanen:
            {chr(10).join([f"- {a['activity']} (Prioritet: {a['priority']}, Status: {a['status']}, Deadline: {a['due_date']})" for a in activities])}

            Checklista status:
            Ledningens engagemang: {', '.join([k for k, v in checklists.get('ledningens_engagemang', {}).items() if v])}
            Scope: {', '.join([k for k, v in checklists.get('scope', {}).items() if v])}
            Riskanalys: {', '.join([k for k, v in checklists.get('riskanalys', {}).items() if v])}

            Baserat på denna information, ge rekommendationer om:
            1. Saknade kritiska aktiviteter som bör läggas till
            2. Förslag på omprioritering av befintliga aktiviteter
            3. Tidslinjejusteringar baserat på best practices
            4. Specifika åtgärder för att öka effektiviteten
            5. Risker att vara uppmärksam på

            Svara på svenska och var mycket specifik i dina rekommendationer.
            Om det saknas aktiviteter, ge konkreta exempel på aktiviteter som bör läggas till.
            """
            
            response = model.generate_content(prompt)
            st.markdown("### 🤖 AI-analys och rekommendationer")
            st.markdown(response.text)
            st.markdown("---")
    
    # Lägg till ny aktivitet
    st.subheader("Lägg till aktivitet")
    col1, col2 = st.columns(2)
    
    with col1:
        new_activity = st.text_input("Aktivitet")
        priority = st.selectbox("Prioritet", ["Hög", "Medium", "Låg"])
    
    with col2:
        due_date = st.date_input("Deadline")
        responsible = st.text_input("Ansvarig")
    
    if st.button("Lägg till aktivitet"):
        if 'activities' not in st.session_state.iso_data:
            st.session_state.iso_data['activities'] = []
        
        st.session_state.iso_data['activities'].append({
            'activity': new_activity,
            'priority': priority,
            'due_date': due_date.strftime('%Y-%m-%d'),
            'responsible': responsible,
            'status': 'Ej påbörjad'
        })
    
    # Visa aktiviteter
    if 'activities' in st.session_state.iso_data and st.session_state.iso_data['activities']:
        st.subheader("Aktiviteter")
        for idx, activity in enumerate(st.session_state.iso_data['activities']):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{activity['activity']}**")
            with col2:
                st.write(f"Prioritet: {activity['priority']}")
            with col3:
                st.write(f"Deadline: {activity['due_date']}")
            with col4:
                status = st.selectbox(
                    "Status",
                    ["Ej påbörjad", "Pågående", "Klar"],
                    key=f"status_{idx}",
                    index=["Ej påbörjad", "Pågående", "Klar"].index(activity['status'])
                )
                activity['status'] = status

    # Spara-knapp för handlingsplan
    if st.button("💾 Spara handlingsplan"):
        if save_data_to_file():
            st.success("Handlingsplan sparad!")

# Exportera Data
elif page == "Exportera Data":
    st.header("💾 Exportera Data")
    
    if st.button("Ladda ner ISO 27001-plan"):
        # Konvertera data till JSON
        json_data = json.dumps(st.session_state.iso_data, indent=2, ensure_ascii=False)
        
        # Skapa nedladdningsbar länk
        st.download_button(
            label="Klicka här för att ladda ner",
            data=json_data,
            file_name=f"iso27001_plan_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
        
        st.success("Din ISO 27001-plan är redo för nedladdning!")

# Footer
st.markdown("---")
st.markdown("*Detta är ett verktyg för att hjälpa till med planering av ISO 27001-certifiering. Det ersätter inte professionell rådgivning.*")
