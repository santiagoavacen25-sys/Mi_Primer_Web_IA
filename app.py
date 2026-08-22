import json
import os
import time
import streamlit as st
from groq import Groq
import tiktoken

# ------------------------------------------------------------------
# 1.  CONSTANTES Y CONFIGURACIÓN
# ------------------------------------------------------------------
ARCHIVO_CHATS = "chats_guardados.json"
MODEL_DEFAULT = "openai/gpt-oss-20b"          # <‑‑ Cambia por "openai/gpt-4o-mini" si tu plan lo permite
MAX_TOKENS = 8000                            # Límite de Groq “on_demand”
MAX_RESPUESTA = 1500                         # Tokens que la IA puede devolver
MAX_HISTORIA = 5                             # Últimos N mensajes que se envían al modelo

# ------------------------------------------------------------------
# 2.  CARGAR Y GUARDAR HISTORIAL
# ------------------------------------------------------------------
def cargar_todos_los_chats():
    return json.load(open(ARCHIVO_CHATS, "r", encoding="utf-8")) if os.path.exists(ARCHIVO_CHATS) else {}

def guardar_todos_los_chats(chats):
    json.dump(chats, open(ARCHIVO_CHATS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ------------------------------------------------------------------
# 3.  ESTIMAR TOKENS (tiktoken)
# ------------------------------------------------------------------
def obtener_tokens(texto: str, model: str = MODEL_DEFAULT) -> int:
    """Devuelve una estimación de tokens para un texto dado."""
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(texto))

def truncar_conversacion(messages, max_tokens=MAX_TOKENS, model=MODEL_DEFAULT):
    """
    Recorta la conversación hasta que la suma de tokens quede por debajo
    de `max_tokens`. Se mantiene el mensaje del sistema y los últimos N
    mensajes de la conversación.
    """
    # Mensaje del sistema
    system_msg = {
        "role": "system",
        "content": (
            "Eres Santi AI, un asistente amigable, claro y útil.\n\n"
            "Responde en español salvo que el usuario pida otro idioma.\n\n"
            "Explica las cosas de forma sencilla cuando el usuario sea principiante."
        )
    }

    # Tomar solo los últimos MAX_HISTORIA mensajes del usuario/IA
    recent = messages[-MAX_HISTORIA:]

    # Construir la lista completa
    msgs = [system_msg] + recent

    # Contar tokens y recortar si es necesario
    total = sum(obtener_tokens(m["content"], model) for m in msgs)
    while total > max_tokens and len(recent) > 1:
        # Eliminar el mensaje más antiguo (el primero de la lista de recientes)
        removed = recent.pop(0)
        total -= obtener_tokens(removed["content"], model)

    return msgs

# ------------------------------------------------------------------
# 4.  CONFIGURACIÓN DE STREAMLIT
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Santi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilos CSS (igual que antes, sin cambios)
st.markdown(
    """
    <style>
    /* ... (copia todo tu bloque CSS) ... */
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# 5.  CONEXIÓN CON GROQ
# ------------------------------------------------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    client = None

if client is None:
    st.error("⚠️ La IA todavía no está configurada.")
    st.info("Configura GROQ_API_KEY en los Secrets de Streamlit.")
    st.stop()

# ------------------------------------------------------------------
# 6.  SESSION STATE
# ------------------------------------------------------------------
todos_los_chats = cargar_todos_los_chats()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.model = MODEL_DEFAULT   # Puedes cambiarlo dinámicamente

# ------------------------------------------------------------------
# 7.  LOGO Y CABECERA
# ------------------------------------------------------------------
if os.path.exists("Logo.jpeg"):
    st.image("Logo.jpeg", use_container_width=False)

st.markdown(
    """
    <div class="welcome">
        <h2>¿En qué puedo ayudarte hoy?</h2
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
# SIDEBAR (HISTORIAL Y NUEVO CHAT)
# =========================================================
with st.sidebar:
    st.title("Santi IA ⚡")
    
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
        chat_actual = todos_los_chats.get(
            st.session_state.current_chat_id,
            {}
        )
        titulo_chat = chat_actual.get(
            "titulo",
            pregunta[:30]
        )

    # ==============================
    # GUARDAR MENSAJE DEL USUARIO
    # ==============================

    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })

    # ==============================
    # MOSTRAR MENSAJE DEL USUARIO
    # ==============================

    with st.chat_message("user", avatar="🧑"):
        st.markdown(pregunta)

    # ==============================
    # RESPUESTA DE LA IA
    # ==============================

    with st.chat_message("assistant", avatar="⚡"):

        area_respuesta = st.empty()

        try:

            # Mensaje del sistema
            mensajes = [
                {
                    "role": "system",
                    "content": """
Eres Santi AI, un asistente amigable,
claro y útil.

Responde en español salvo que
el usuario pida otro idioma.

Explica las cosas de forma sencilla
cuando el usuario sea principiante.
"""
                }
            ]

            # Solo enviamos los últimos 10 mensajes
            mensajes.extend(
                st.session_state.messages[-6:]
            )

            # ==============================
            # LLAMADA A GROQ
            # ==============================

            respuesta = client.chat.completions.create(
                model=st.session_state.model,
                messages=mensajes,
                temperature=0.7,
                max_tokens=1500
            )

            # ==============================
            # OBTENER RESPUESTA
            # ==============================

            texto = respuesta.choices[0].message.content

            area_respuesta.markdown(texto)

            # Intentar colocar la respuesta arriba
            colocar_respuesta_arriba()

            # ==============================
            # GUARDAR RESPUESTA
            # ==============================

            st.session_state.messages.append({
                "role": "assistant",
                "content": texto
            })

            # ==============================
            # GUARDAR CHAT
            # ==============================

            todos_los_chats[
                st.session_state.current_chat_id
            ] = {
                "titulo": titulo_chat,
                "messages": st.session_state.messages
            }

            guardar_todos_los_chats(
                todos_los_chats
            )

        except Exception as e:

            area_respuesta.error(
                "❌ Ocurrió un error al conectar con la IA."
            )

            st.code(str(e))

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    Santi IA ⚡ · Python + Streamlit + Groq
</div>
""", unsafe_allow_html=True)