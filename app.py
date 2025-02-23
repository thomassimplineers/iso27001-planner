import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

# Ladda miljövariabler
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Testa API-anslutning
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('Ping test: Svara "OK" om du får detta meddelande.')
    st.success("✅ API-anslutning fungerar!")
    st.write("Svar från API:", response.text)
except Exception as e:
    st.error(f"❌ Kunde inte ansluta till API:et. Fel: {str(e)}")

# Konfigurera Streamlit sida
st.set_page_config(
    page_title="Gemini API Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS för bättre design
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
    }
    .output-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Gemini AI Studio Demo")
st.markdown("---")

# Sidmeny med ikoner
demo_type = st.sidebar.selectbox(
    "📱 Välj Demo",
    ["✍️ Text Generation (Gemini Pro)", 
     "🖼️ Vision (Gemini Pro Vision)", 
     "💬 Chat (Gemini Pro)"]
)

# Text Generation Demo
def text_generation_demo():
    st.header("✍️ Text Generation med Gemini Pro")
    st.markdown("Skriv en prompt för att generera text med Gemini Pro.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        prompt = st.text_area("Din prompt:", height=150, 
                             placeholder="Exempel: Skriv en kort dikt om AI...")
    with col2:
        st.markdown("### Tips 💡")
        st.markdown("""
        - Var specifik i din prompt
        - Ange önskat format
        - Specificera ton och stil
        """)
    
    if st.button("🚀 Generera"):
        if prompt:
            with st.spinner("✨ Genererar svar..."):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    st.markdown("### Resultat")
                    st.markdown('<div class="output-container">', unsafe_allow_html=True)
                    st.markdown(response.text)
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Ett fel uppstod: {str(e)}")
        else:
            st.warning("⚠️ Skriv en prompt först!")

# Vision Demo
def vision_demo():
    st.header("🖼️ Vision Demo med Gemini Pro Vision")
    st.markdown("Ladda upp en bild och ställ frågor om den.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("📤 Ladda upp en bild", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Din bild", use_column_width=True)
    
    with col2:
        prompt = st.text_area("Din fråga om bilden:", height=150,
                             placeholder="Exempel: Beskriv vad som händer i bilden...")
        if uploaded_file and prompt:
            if st.button("🔍 Analysera"):
                with st.spinner("🤔 Analyserar bild..."):
                    try:
                        model = genai.GenerativeModel('gemini-pro-vision')
                        response = model.generate_content([prompt, image])
                        st.markdown("### Analys")
                        st.markdown('<div class="output-container">', unsafe_allow_html=True)
                        st.markdown(response.text)
                        st.markdown('</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Ett fel uppstod: {str(e)}")

# Chat Demo
def chat_demo():
    st.header("💬 Chat med Gemini Pro")
    st.markdown("Ha en interaktiv konversation med AI:n.")
    
    # Initiera chat-historik i session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat = genai.GenerativeModel('gemini-pro').start_chat(history=[])

    # Visa chat-historik
    for message in st.session_state.messages:
        role = "🤖 AI" if message["role"] == "assistant" else "👤 Du"
        with st.chat_message(message["role"]):
            st.markdown(f"**{role}:** {message['content']}")

    # Chat input
    prompt = st.chat_input("Skriv ditt meddelande...")
    if prompt:
        # Visa användarens meddelande
        with st.chat_message("user"):
            st.markdown(f"👤 **Du:** {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generera och visa AI:s svar
        with st.chat_message("assistant"):
            with st.spinner("🤔 Tänker..."):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.markdown(f"🤖 **AI:** {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Ett fel uppstod: {str(e)}")

# Kör vald demo
if not GOOGLE_API_KEY:
    st.error("❌ Ingen API-nyckel hittad. Skapa en .env fil med din GOOGLE_API_KEY.")
else:
    # Ta bort emoji från demo_type för att matcha
    clean_demo_type = demo_type.split(" ")[1:]
    clean_demo_type = " ".join(clean_demo_type)
    
    if "Text Generation" in clean_demo_type:
        text_generation_demo()
    elif "Vision" in clean_demo_type:
        vision_demo()
    elif "Chat" in clean_demo_type:
        chat_demo()

# Lägg till information i sidebaren
with st.sidebar:
    st.markdown("### Om Modellerna")
    st.markdown("""
    - **Gemini Pro**: Textgenerering och analys
    - **Gemini Pro Vision**: Bildanalys och beskrivning
    - **Gemini Pro (Chat)**: Interaktiv konversation
    """)
    
    st.markdown("### Tips")
    st.markdown("""
    - Testa olika typer av prompts
    - Jämför resultaten mellan modellerna
    - Experimentera med bildanalys
    """)
