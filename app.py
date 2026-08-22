import json
import os
import time
import streamlit as st
from groq import Groq

# =========================================================
# ARCHIVO DE HISTORIAL
# =========================================================
ARCHIVO_CHATS = "chats_guardados.json"

def cargar_todos_los_chats():
    if os.path.exists(ARCHIVO_CHATS):
        try:
            with open(ARCHIVO_CHATS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def guardar_todos_los_chats(chats):
    with open(ARCHIVO_CHATS, "w", encoding="utf-8") as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)

# =========================================================
# CONFIGURACIÓN DE PÁGINA
# =========================================================
st.set_page_config(
    page_title="Santi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILOS CSS Y PARCHE JAVASCRIPT (ANTI-AUTO SCROLL)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    overflow-anchor: none !important;
    scroll-behavior: auto !important;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(120, 80, 255, 0.18), transparent 30%),
        radial-gradient(circle at 85% 20%, rgba(0, 180, 255, 0.12), transparent 30%),
        linear-gradient(135deg, #070912 0%, #0b1020 50%, #070912 100%);
    color: white;
}

.block-container {
    padding-top: 2rem !important; 
    padding-bottom: 5rem !important;
    max-width: 1100px;
}

section[data-testid="stSidebar"] {
    background-color: rgba(18, 20, 26, 0.8) !important;
    backdrop-filter: blur(12px) !important;
}

header[data-testid="stHeader"]{
    background: transparent !important;
}

div[data-testid="stImage"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin-bottom: 25px !important;
}

div[data-testid="stImage"] img {
    background: rgba(20, 20, 35, 0.6) !important;
    border-radius: 24px !important;
    padding: 15px !important;
    border: 1px solid rgba(140, 80, 255, 0.3) !important;
    box-shadow: 0 0 25px rgba(120, 80, 255, 0.3) !important;
    transition: all 0.3s ease !important;
    object-fit: contain !important;
    max-width: 210px !important;
    width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
}

div[data-testid="stImage"] img:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 0 40px rgba(140, 80, 255, 0.6) !important;
}

.welcome {
    text-align: center;
    padding: 15px;
    margin-top: 10px;
    margin-bottom: 20px;
}

.welcome h2 {
    font-size: 28px;
    margin-bottom: 8px;
}

.welcome p {
    color: #8e96aa;
    font-size: 15px;
}

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.07);
    color: white;
    font-weight: 600;
    padding: 10px 16px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.13);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-1px);
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    margin-bottom: 10px;
}

[data-testid="stChatInput"] {
    border-radius: 18px;
}

.footer {
    text-align: center;
    color: #737b91;
    font-size: 13px;
    padding: 30px 0 10px 0;
}

@media (max-width: 768px) {
    .stTextInput input, .stTextArea textarea {
        font-size: 16px !important;
    }
}
</style>

<script>
// Bloquea las llamadas automáticas de Streamlit para hacer scroll hacia abajo
Element.prototype.scrollIntoView = function() {};
</script>
""", unsafe_allow_html=True)

# =========================================================
# GROQ CONEXIÓN
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    client = None

# =========================================================
# SESSION STATE E HISTORIAL
# =========================================================
todos_los_chats = cargar_todos_los_chats()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# MODELO OFICIAL VIGENTE EN GROQ
st.session_state.model = "openai/gpt-oss-20b"

# =========================================================
# LOGO Y CABECERA
# =========================================================
if os.path.exists("Logo.jpeg"):
    st.image("Logo.jpeg", use_container_width=False)

st.markdown("""
<div class="welcome">
    <h2>¿En qué puedo ayudarte hoy?</h2>
    <p>
        Pregúntame sobre programación, tecnología,
        videojuegos, aprendizaje o cualquier otra cosa.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# COMPROBAR API
# =========================================================
if client is None:
    st.error("⚠️ La IA todavía no está configurada.")
    st.info("Configura GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# =========================================================
# PROCESAR NUEVO MENSAJE Y GUARDADO AUTOMÁTICO
# =========================================================
pregunta = st.chat_input("Escribe tu pregunta para Santi IA...")

if pregunta:
    if st.session_state.current_chat_id is None:
        st.session_state.current_chat_id = str(int(time.time()))
        titulo_chat = pregunta[:30] if len(pregunta) > 30 else pregunta
    else:
        chat_actual = todos_los_chats.get(st.session_state.current_chat_id, {})
        titulo_chat = chat_actual.get("titulo", pregunta[:30])

    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(pregunta)

    # Generar respuesta de la IA
    with st.chat_message("assistant", avatar="⚡"):
        # 1. Contenedor vacío para la respuesta
        area_respuesta = st.empty()
        texto = None
        
        # 2. Spinner solo mientras consulta a Groq
        with st.spinner("Pensando..."):
            try:
                mensajes = [
                    {
                        "role": "system",
                        "content": "Eres Santi AI, un asistente amigable, claro y útil. Responde en español salvo que el usuario pida otro idioma."
                    }
                ]
                mensajes.extend(st.session_state.messages)

                respuesta = client.chat.completions.create(
                    model=st.session_state.model,
                    messages=mensajes,
                    temperature=0.7,
                    max_tokens=2048
                )

                texto = respuesta.choices[0].message.content

            except Exception as e:
                st.error("❌ Ocurrió un error al conectar con la IA.")
                st.code(str(e))

        # 3. Dibujar el texto FUERA del spinner
        if texto:
            area_respuesta.markdown(texto)

            st.session_state.messages.append({
                "role": "assistant",
                "content": texto
            })

            todos_los_chats[st.session_state.current_chat_id] = {
                "titulo": titulo_chat,
                "messages": st.session_state.messages
            }
            guardar_todos_los_chats(todos_los_chats)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
Santi IA ⚡ · Python + Streamlit + Groq
</div>
""", unsafe_allow_html=True)