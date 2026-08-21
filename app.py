import json
import os
import streamlit as st
from groq import Groq

# =========================================================
# CARGA AUTOMÁTICA DEL HISTORIAL
# =========================================================
if "messages" not in st.session_state:
    if os.path.exists("chats_guardados.json"):
        with open("chats_guardados.json", "r") as archivo:
            st.session_state.messages = json.load(archivo)
    else:
        st.session_state.messages = []

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILOS CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
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
    padding-top: 7rem !important; 
    padding-bottom: 2rem;
    max-width: 1100px;
}

section[data-testid="stSidebar"] {
    background-color: rgba(18 , 20, 26, 0.2) !important;
    backdrop-filter: blur(12px) !important;
}

header[data-testid="stHeader"]{
    background: transparent !important;
    background-color: rgba(18, 20, 26, 0.2) !important;    
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

@media (max-width: 768px) {
    .block-container {
        padding-top: 2rem !important;
    }
    div[data-testid="stImage"] img {
        max-width: 150px !important;
        padding: 10px !important;
    }
}

.hero {
    text-align: center;
    padding: 35px 20px 25px 20px;
}

.glass {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 22px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.18);
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

.small {
    color: #8e96aa;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO Y CABECERA
# =========================================================
st.image("Logo.jpeg", use_container_width=False)

# =========================================================
# GROQ CONECTION
# =========================================================
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    client = None

# =========================================================
# SESSION STATE
# =========================================================
if "model" not in st.session_state:
    st.session_state.model = "llama3-70b-8192"
    
if "chats" not in st.session_state:
    st.session_state.chats = {} 

# =========================================================
# COMPROBAR API
# =========================================================
if client is None:
    st.error("⚠️ La IA todavía no está configurada.")
    st.info("Configura GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# =========================================================
# PANEL PRINCIPAL
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="glass">
<div style="font-size:28px;">🤖</div>
<h3>Chat con IA</h3>
<div class="small">Pregunta lo que quieras y recibe respuestas.</div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="glass">
<div style="font-size:28px;">💻</div>
<h3>Programación</h3>
<div class="small">Aprende Python, web, APIs y mucho más.</div>
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="glass">
<div style="font-size:28px;">📚</div>
<h3>Aprendizaje</h3>
<div class="small">Explicaciones sencillas paso a paso.</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("⚙️ Configuración")
    st.divider()

    if st.button("➕ Nuevo chat"):
        st.session_state.messages = []
        if os.path.exists("chats_guardados.json"):
            os.remove("chats_guardados.json")
        st.rerun()

    st.divider()
    st.caption("Santi AI ⚡")

# =========================================================
# SUGERENCIAS
# =========================================================
if len(st.session_state.messages) == 0:
    st.markdown("""
<div class="glass">
<h3>👋 ¿Qué quieres hacer?</h3>
<p class="small">
Puedes preguntarme sobre programación,
videojuegos, tecnología, tareas,
matemáticas, ideas para proyectos
o prácticamente cualquier tema.
</p>
</div>
""", unsafe_allow_html=True)

    st.write("")
    a, b, c = st.columns(3)

    with a:
        if st.button("🐍 Enséñame Python"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Enséñame Python desde cero con un ejercicio sencillo."
            })
            st.rerun()

    with b:
        if st.button("💻 Dame un proyecto"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Dame una idea de proyecto de programación que pueda hacer siendo principiante."
            })
            st.rerun()

    with c:
        if st.button("🚀 Explícame IA"):
            st.session_state.messages.append({
                "role": "user",
                "content": "Explícame qué es la inteligencia artificial de forma sencilla."
            })
            st.rerun()

# =========================================================
# HISTORIAL EN PANTALLA
# =========================================================
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "⚡"
    ):
        st.markdown(message["content"])

# =========================================================
# CHAT Y RESPUESTA DE LA IA
# =========================================================
pregunta = st.chat_input("Escribe tu pregunta para Santi IA...")

if pregunta:
    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(pregunta)

    with st.chat_message("assistant", avatar="⚡"):
        try:
            with st.spinner("Pensando..."):
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
                st.markdown(texto)

                # Guardar respuesta en la sesión
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": texto
                })

                # GUARDADO AUTOMÁTICO EN EL ARCHIVO JSON
                with open("chats_guardados.json", "w") as archivo:
                    json.dump(st.session_state.messages, archivo)

        except Exception as e:
            st.error("❌ Ocurrió un error al conectar con la IA.")
            st.code(str(e))

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
Santi IA ⚡ · Python + Streamlit + Groq
</div>
""", unsafe_allow_html=True)