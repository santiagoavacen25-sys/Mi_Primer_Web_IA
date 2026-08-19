import streamlit as st
from groq import Groq

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Santi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DISEÑO
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(120, 70, 255, 0.20), transparent 30%),
        radial-gradient(circle at 90% 15%, rgba(0, 180, 255, 0.15), transparent 30%),
        linear-gradient(135deg, #060811 0%, #0b1020 50%, #05070e 100%);
    color: white;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ================= HEADER ================= */

.hero {
    text-align: center;
    padding: 25px 20px 30px 20px;
}

.logo {
    width: 72px;
    height: 72px;
    margin: auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 22px;

    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.13);

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    font-size: 36px;

    box-shadow:
        0 15px 50px rgba(0,0,0,0.30);
}

.hero h1 {
    margin-top: 18px;
    margin-bottom: 8px;

    font-size: 44px;
    font-weight: 800;
    letter-spacing: -2px;
}

.hero p {
    color: #aab2c7;
    font-size: 16px;
}

/* ================= GLASS ================= */

.glass {
    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 22px;

    padding: 22px;

    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);

    box-shadow:
        0 15px 45px rgba(0,0,0,0.18);
}

/* ================= BOTONES ================= */

.stButton > button {
    width: 100%;

    border-radius: 14px;

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.12);

    color: white;

    font-weight: 600;

    transition: 0.2s;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.12);

    border-color: rgba(255,255,255,0.25);

    transform: translateY(-1px);
}

/* ================= CHAT ================= */

[data-testid="stChatMessage"] {

    background: rgba(255,255,255,0.045);

    border: 1px solid rgba(255,255,255,0.07);

    border-radius: 18px;

    margin-bottom: 12px;
}

/* ================= INPUT ================= */

[data-testid="stChatInput"] {
    border-radius: 18px;
}

/* ================= SELECT ================= */

div[data-baseweb="select"] > div {

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.12);

    border-radius: 14px;
}

/* ================= TEXTO ================= */

.small {
    color: #8e96aa;
    font-size: 13px;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;

    color: #70788c;

    font-size: 13px;

    padding-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CONEXIÓN CON GROQ
# =========================================================

try:

    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(
        api_key=api_key
    )

except Exception:

    client = None


# =========================================================
# SESIÓN
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

    <div class="logo">
        ⚡
    </div>

    <h1>Santi AI</h1>

    <p>
        Tu asistente de inteligencia artificial para aprender,
        programar, crear y resolver problemas.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# COMPROBAR API
# =========================================================

if client is None:

    st.error(
        "⚠️ No se encontró GROQ_API_KEY."
    )

    st.info(
        "Ve a los Secrets de Streamlit y agrega tu clave de Groq."
    )

    st.stop()


# =========================================================
# INFORMACIÓN
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="glass">

        <div style="font-size:30px;">
            🤖
        </div>

        <h3>Chat con IA</h3>

        <div class="small">
            Pregunta lo que quieras y recibe respuestas.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="glass">

        <div style="font-size:30px;">
            💻
        </div>

        <h3>Programación</h3>

        <div class="small">
            Aprende Python, páginas web, APIs y más.
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="glass">

        <div style="font-size:30px;">
            📚
        </div>

        <h3>Aprendizaje</h3>

        <div class="small">
            Explicaciones sencillas paso a paso.
        </div>

    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Configuración")

    st.markdown(
        "**Modelo:**"
    )

    st.code(
        "llama-3.3-70b-versatile"
    )

    st.caption(
        "Modelo utilizado por Santi AI"
    )

    st.divider()

    if st.button("🗑️ Borrar conversación"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("⚡ Santi AI")

    st.caption(
        "Python + Streamlit + Groq"
    )


# =========================================================
# BIENVENIDA
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown("""
    <div class="glass">

        <h3>
            👋 ¡Hola!
        </h3>

        <p class="small">
            Soy Santi AI. Puedes preguntarme sobre programación,
            tecnología, videojuegos, tareas, matemáticas,
            proyectos o cualquier tema.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🐍 Enséñame Python"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Enséñame Python desde cero con un ejercicio sencillo."
            })

            st.rerun()


    with col2:

        if st.button("💻 Dame un proyecto"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Dame una idea de proyecto de programación para un principiante."
            })

            st.rerun()


    with col3:

        if st.button("🤖 Explícame la IA"):

            st.session_state.messages.append({
                "role": "user",
                "content": "Explícame qué es la inteligencia artificial de forma sencilla."
            })

            st.rerun()


# =========================================================
# MOSTRAR HISTORIAL
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        avatar = "🧑"

    else:

        avatar = "⚡"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT
# =========================================================

pregunta = st.chat_input(
    "Escribe tu pregunta para Santi AI..."
)


if pregunta:

    # -----------------------------------------
    # GUARDAR MENSAJE DEL USUARIO
    # -----------------------------------------

    st.session_state.messages.append({

        "role": "user",

        "content": pregunta

    })


    # -----------------------------------------
    # MOSTRAR MENSAJE
    # -----------------------------------------

    with st.chat_message(
        "user",
        avatar="🧑"
    ):

        st.markdown(
            pregunta
        )


    # -----------------------------------------
    # RESPUESTA IA
    # -----------------------------------------

    with st.chat_message(
        "assistant",
        avatar="⚡"
    ):

        try:

            with st.spinner(
                "Pensando..."
            ):

                # Prompt del sistema
                system_message = {

                    "role": "system",

                    "content": """
Eres Santi AI.

Eres un asistente de inteligencia artificial
amigable, útil y fácil de entender.

Responde en español por defecto.

Tu objetivo es ayudar al usuario a:

- aprender programación
- aprender Python
- crear páginas web
- resolver problemas
- aprender tecnología
- crear proyectos
- entender videojuegos
- estudiar
- generar ideas

REGLAS:

1. Explica las cosas de forma sencilla.

2. Si el usuario es principiante,
   evita utilizar palabras demasiado técnicas
   sin explicarlas.

3. Si pide código,
   proporciona código funcional.

4. Si hay varias maneras de solucionar algo,
   recomienda primero la más sencilla.

5. Si detectas un error en código,
   explica qué está causando el error
   y cómo solucionarlo.

6. No inventes información.

7. Si no estás seguro de algo,
   dilo claramente.

8. No seas innecesariamente largo.

9. Mantén un tono amigable.

10. Cuando expliques programación,
    intenta incluir ejemplos prácticos.
"""
                }


                # -----------------------------------------
                # CREAR MENSAJES
                # -----------------------------------------

                mensajes = [

                    system_message

                ] + st.session_state.messages


                # -----------------------------------------
                # LLAMAR A GROQ
                # -----------------------------------------

                respuesta = client.chat.completions.create(

                    model="llama-3.3-70b-versatile",

                    messages=mensajes,

                    temperature=0.7,

                    max_completion_tokens=2048

                )


                # -----------------------------------------
                # OBTENER TEXTO
                # -----------------------------------------

                texto = (
                    respuesta
                    .choices[0]
                    .message
                    .content
                )


                # -----------------------------------------
                # MOSTRAR RESPUESTA
                # -----------------------------------------

                st.markdown(
                    texto
                )


                # -----------------------------------------
                # GUARDAR RESPUESTA
                # -----------------------------------------

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": texto

                })


        except Exception as e:

            st.error(
                "❌ Ocurrió un error al conectar con la IA."
            )

            st.code(
                str(e)
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    ⚡ Santi AI

    <br>

    Python · Streamlit · Groq

    <br><br>

    Una IA creada para aprender, programar y crear.

</div>
""", unsafe_allow_html=True)