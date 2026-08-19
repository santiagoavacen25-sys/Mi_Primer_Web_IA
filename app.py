import os
import streamlit as st
from groq import Groq


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Santi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ESTILOS
# =========================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #070b16;
    --panel: rgba(255,255,255,0.055);
    --panel-hover: rgba(255,255,255,0.085);
    --border: rgba(255,255,255,0.10);
    --text: #f5f7ff;
    --muted: #9ca7bd;
    --accent: #7c5cff;
    --accent2: #00d4ff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(124,92,255,0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(0,212,255,0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #070b16 0%,
            #0a1020 50%,
            #060914 100%
        );
    color: var(--text);
}

/* Quitar espacio superior */
.block-container {
    padding-top: 2rem;
    padding-bottom: 7rem;
    max-width: 1200px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(20,25,42,0.96),
            rgba(8,11,22,0.98)
        );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #f4f6ff;
}

/* HEADER */

.hero {
    padding: 35px;
    border: 1px solid var(--border);
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            rgba(124,92,255,0.13),
            rgba(0,212,255,0.06)
        );
    backdrop-filter: blur(20px);
    margin-bottom: 25px;
}

.hero-logo {
    width: 58px;
    height: 58px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(
            135deg,
            var(--accent),
            var(--accent2)
        );
    font-size: 28px;
    margin-bottom: 18px;
    box-shadow: 0 10px 35px rgba(124,92,255,0.30);
}

.hero h1 {
    margin: 0;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero p {
    margin-top: 10px;
    color: var(--muted);
    font-size: 16px;
}

/* TARJETAS */

.feature-card {
    padding: 25px;
    min-height: 150px;
    border-radius: 20px;
    border: 1px solid var(--border);
    background: var(--panel);
    backdrop-filter: blur(18px);
    transition: 0.2s ease;
}

.feature-card:hover {
    background: var(--panel-hover);
    border-color: rgba(124,92,255,0.35);
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 20px;
    font-weight: 700;
}

.feature-text {
    color: var(--muted);
    font-size: 14px;
    margin-top: 8px;
}

/* BOTONES */

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    transition: 0.2s ease !important;
}

.stButton > button:hover {
    border-color: var(--accent) !important;
    background: rgba(124,92,255,0.14) !important;
}

/* CHAT */

div[data-testid="stChatMessage"] {
    border: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.035);
    border-radius: 18px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
}

/* INPUT */

div[data-testid="stChatInput"] {
    border-radius: 18px;
}

div[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    color: white !important;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #69748c;
    font-size: 13px;
    margin-top: 45px;
}

/* OCULTAR COSAS INNECESARIAS */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""")


# =========================================================
# CONFIGURACIÓN DE GROQ
# =========================================================

MODEL = "llama-3.3-70b-versatile"


def get_api_key():
    """
    Primero intenta obtener la clave desde Streamlit Secrets.
    Si no existe, intenta obtenerla desde una variable de entorno.
    """

    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


api_key = get_api_key()


# =========================================================
# CLIENTE GROQ
# =========================================================

client = None

if api_key:
    client = Groq(api_key=api_key)


# =========================================================
# MEMORIA DEL CHAT
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚙️ Configuración")

    st.caption("Modelo de IA")

    st.info(
        f"**{MODEL}**\n\n"
        "Modelo de lenguaje de Groq."
    )

    st.divider()

    if st.button(
        "🗑️ Borrar conversación",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### ⚡ Santi AI")

    st.caption(
        "Tu asistente personal para programación, "
        "tecnología, videojuegos, aprendizaje y proyectos."
    )

    st.divider()

    if client:
        st.success("🟢 IA conectada")
    else:
        st.error("🔴 Falta GROQ_API_KEY")


# =========================================================
# HEADER
# =========================================================

st.html("""
<div class="hero">

    <div class="hero-logo">
        ⚡
    </div>

    <h1>Santi AI</h1>

    <p>
        Tu asistente de inteligencia artificial para aprender,
        programar, crear proyectos y resolver problemas.
    </p>

</div>
""")


# =========================================================
# TARJETAS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.html("""
    <div class="feature-card">

        <div class="feature-icon">🤖</div>

        <div class="feature-title">
            Chat con IA
        </div>

        <div class="feature-text">
            Pregunta lo que quieras y recibe respuestas
            generadas por inteligencia artificial.
        </div>

    </div>
    """)


with col2:
    st.html("""
    <div class="feature-card">

        <div class="feature-icon">💻</div>

        <div class="feature-title">
            Programación
        </div>

        <div class="feature-text">
            Aprende Python, páginas web, APIs,
            proyectos y mucho más.
        </div>

    </div>
    """)


with col3:
    st.html("""
    <div class="feature-card">

        <div class="feature-icon">📚</div>

        <div class="feature-title">
            Aprendizaje
        </div>

        <div class="feature-text">
            Explicaciones sencillas y paso a paso
            para aprender más rápido.
        </div>

    </div>
    """)


st.write("")


# =========================================================
# MENSAJE INICIAL
# =========================================================

if not st.session_state.messages:

    st.html("""
    <div class="feature-card">

        <div class="feature-icon">👋</div>

        <div class="feature-title">
            ¡Hola!
        </div>

        <div class="feature-text">
            Soy Santi AI. Puedes preguntarme sobre
            programación, Python, tecnología, videojuegos,
            tareas, matemáticas, proyectos o cualquier otro tema.
        </div>

    </div>
    """)


# =========================================================
# MOSTRAR CONVERSACIÓN
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# BOTONES RÁPIDOS
# =========================================================

st.write("")

q1, q2, q3 = st.columns(3)

quick_prompt = None


with q1:
    if st.button(
        "🐍 Enséñame Python",
        use_container_width=True
    ):
        quick_prompt = (
            "Enséñame Python desde cero. "
            "Quiero aprender de forma práctica y con ejercicios."
        )


with q2:
    if st.button(
        "💻 Dame un proyecto",
        use_container_width=True
    ):
        quick_prompt = (
            "Dame un proyecto de programación para principiantes "
            "que pueda hacer en Python y explícame cómo empezar."
        )


with q3:
    if st.button(
        "🤖 Explícame la IA",
        use_container_width=True
    ):
        quick_prompt = (
            "Explícame qué es la inteligencia artificial "
            "de una manera sencilla y dime cómo puedo empezar "
            "a programarla."
        )


# =========================================================
# FUNCIÓN PARA PREGUNTAR A GROQ
# =========================================================

def ask_ai(user_message):

    system_prompt = """
Eres Santi AI, un asistente amigable y útil.

Tu objetivo es ayudar especialmente con:

- programación
- Python
- desarrollo web
- inteligencia artificial
- tecnología
- videojuegos
- computadoras
- aprendizaje
- proyectos

Habla en español.

Explica las cosas de forma clara y sencilla.

Si el usuario está aprendiendo programación:
- explica paso a paso
- utiliza ejemplos
- no asumas conocimientos avanzados
- corrige errores sin burlarte

Si das código:
- utiliza bloques de código
- explica para qué sirve
- procura que el código sea funcional

No inventes información cuando no estés seguro.
"""


    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(
        st.session_state.messages
    )

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2048
    )

    return response.choices[0].message.content


# =========================================================
# CHAT INPUT
# =========================================================

user_prompt = st.chat_input(
    "Escribe tu pregunta para Santi AI..."
)


# =========================================================
# DETERMINAR MENSAJE
# =========================================================

prompt = user_prompt or quick_prompt


# =========================================================
# PROCESAR MENSAJE
# =========================================================

if prompt:

    # Mostrar mensaje del usuario
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # Comprobar API
    if not client:

        error_message = """
### ⚠️ Falta configurar Groq

No encontré `GROQ_API_KEY`.

Si estás usando Streamlit Cloud:

1. Ve a **Manage app**.
2. Abre **Settings**.
3. Entra en **Secrets**.
4. Agrega:

```toml
GROQ_API_KEY = "TU_CLAVE_DE_GROQ"