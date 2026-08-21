import json
import os
import time
import streamlit as st
from groq import Groq

# =========================================================
# CONFIGURACIÓN DE PÁGINA (Solo debe ejecutarse UNA vez)
# =========================================================
st.set_page_config(
    page_title="Santi AI Mobile",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"  # En celular inicia cerrada para comodidad
)

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
# ESTILOS CSS (Logo personalizado + Optimización Móvil)
# =========================================================
URL_MI_LOGO = "https://i.imgur.com/v04Xk4J.png"  # Cambia esta URL por la directa de tu logo

st.markdown(f"""
    <style>
    /* --------------------------------------------------
       1. REEMPLAZO DE FLECHA DE BARRA LATERAL POR TU LOGO
       -------------------------------------------------- */
    button[data-testid="stSidebarCollapseButton"] svg,
    button[data-testid="stHeaderCollapsedControl"] svg {{
        display: none !important;
    }}

    button[data-testid="stSidebarCollapseButton"] {{
        background-image: url("{URL_MI_LOGO}") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 40px !important;
        height: 40px !important;
        border: none !important;
    }}

    button[data-testid="stHeaderCollapsedControl"] {{
        background-image: url("{URL_MI_LOGO}") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 40px !important;
        height: 40px !important;
        border: none !important;
        margin-left: 8px !important;
        margin-top: 4px !important;
    }}

    button[data-testid="stHeaderCollapsedControl"]:active, 
    button[data-testid="stSidebarCollapseButton"]:active {{
        transform: scale(0.92);
        transition: transform 0.1s ease;
    }}

    /* --------------------------------------------------
       2. OPTIMIZACIÓN TÁCTIL / MOBILE-FIRST
       -------------------------------------------------- */
    /* Relleno cómodo en pantallas chicas */
    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }}

    /* Botones grandes y fáciles de tocar con el pulgar */
    .stButton > button {{
        width: 100% !important;
        height: 3.2rem !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
    }}

    /* Evita que los iPhone / Android hagan zoom al tocar para escribir */
    .stTextInput input, .stTextArea textarea {{
        font-size: 16px !important;
        border-radius: 10px !important;
    }}

    /* Ajuste del sidebar en celular para que no ocupe todo el ancho */
    @media (max-width: 768px) {{
        section[data-testid="stSidebar"] {{
            width: 82vw !important;
        }}
        header {{
            background: transparent !important;
        }}
    }}
    </style>
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

# MODELO ACTIVO EN GROQ (ACTUALIZADO)
st.session_state.model = "openai/gpt-oss-20b"

# =========================================================
# LOGO Y CABECERA
# =========================================================
st.image("Logo.jpeg", use_container_width=False)

# =========================================================
# COMPROBAR API
# =========================================================
if client is None:
    st.error("⚠️ La IA todavía no está configurada.")
    st.info("Configura GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# =========================================================
# SIDEBAR (HISTORIAL Y NUEVO CHAT)
# =========================================================
with st.sidebar:
    st.title("⚙️ Menú")
    
    if st.button("➕ Nuevo chat", use_container_width=True):
        st.session_state.current_chat_id = None
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### 💬 Historial de Chats")

    if todos_los_chats:
        for chat_id, chat_data in reversed(list(todos_los_chats.items())):
            titulo = chat_data.get("titulo", "Chat sin título")
            if len(titulo) > 28:
                titulo = titulo[:25] + "..."
            
            es_activo = (st.session_state.current_chat_id == chat_id)
            label = f"📌 {titulo}" if es_activo else f"💬 {titulo}"
            
            if st.button(label, key=f"chat_{chat_id}", use_container_width=True):
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = chat_data.get("messages", [])
                st.rerun()
    else:
        st.caption("Aún no hay chats guardados.")

    st.divider()
    st.caption("Santi AI ⚡")

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
# SUGERENCIAS INICIALES
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
# MOSTRAR MENSAJES EN PANTALLA
# =========================================================
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "⚡"
    ):
        st.markdown(message["content"])

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

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": texto
                })

                todos_los_chats[st.session_state.current_chat_id] = {
                    "titulo": titulo_chat,
                    "messages": st.session_state.messages
                }
                guardar_todos_los_chats(todos_los_chats)
                st.rerun()

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