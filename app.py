import streamlit as st
from groq import Groq

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOGO Y CABECERA
# =========================================================

# Las 3 columnas para centrar la imagen en la pantalla 
# Las 3 columnas para centrar la imagen en la pantalla 
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("Logo.jpeg", use_container_width=False)

# =========================================================
# ESTILOS
# =========================================================

# =========================================================
# LOGO Y CABECERA (HERO)
# =========================================================

# Inyectamos el CSS para centrar absolutamente todo el bloque hero
st.markdown("""
<style>
.hero-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    margin: 10px 0 30px 0;
}

.hero-logo-card {
    background: rgba(20, 20, 35, 0.6);
    border-radius: 28px;
    padding: 18px;
    border: 1px solid rgba(140, 80, 255, 0.35);
    box-shadow: 0 0 30px rgba(120, 80, 255, 0.3);
    transition: all 0.4s ease;
    display: inline-block;
    cursor: pointer;
}

.hero-logo-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 
        -10px 0 30px #00f3ff, 
        10px 0 30px #ff00ff,
        0 0 50px rgba(0, 243, 255, 0.8);
}

.hero-logo-card img {
    max-width: 180px;
    height: auto;
    border-radius: 18px;
    display: block;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-top: 15px;
    background: linear-gradient(90deg, #ffffff 0%, #aeb6cc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}
</style>

<div class="hero-container">
    <div class="hero-logo-card">
        <img src="https://raw.githubusercontent.com/streamlit/streamlit/main/docs/static/logo.png" alt="Logo" id="logo-img">
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# GROQ
# =========================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(
        api_key=api_key
    )

except Exception:
    client = None


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "openai/gpt-oss-120b"
    
if "chats" not in st.session_state:
    st.session_state.chats = {} 


# =========================================================
# COMPROBAR API
# =========================================================

if client is None:

    st.error(
        "⚠️ La IA todavía no está configurada."
    )

    st.info(
        "Configura GROQ_API_KEY en los Secrets de Streamlit."
    )

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

    # 1. BOTÓN PARA BORRAR / NUEVO CHAT
    if st.button("➕ Nuevo chat"):
        st.session_state.messages = []
        st.rerun()

    # 2. BOTÓN PARA GUARDAR
    if st.button("💾 Guardar chat"):
        if len(st.session_state.messages) > 0:
            num = len(st.session_state.chats) + 1
            st.session_state.chats[f"Chat {num}"] = st.session_state.messages.copy()
            st.success(f"Guardado como Chat {num}")
        else:
            st.warning("No hay nada que guardar.")

    st.divider()
    st.subheader("Mis Chats Guardados")

    # BUCLE FOR PARA MOSTRAR Y ELIMINAR CHATS
    for nombre_chat in list(st.session_state.chats):
        if st.button(f"💬 {nombre_chat}"):
            st.session_state.messages = st.session_state.chats[nombre_chat]
            st.rerun() 
          
        if st.button(f"🗑️ Borrar {nombre_chat}"):
            del st.session_state.chats[nombre_chat]        
            st.rerun()
        
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
# HISTORIAL
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "⚡"
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT
# =========================================================

pregunta = st.chat_input(
    "Escribe tu pregunta para Santi IA..."
)

if pregunta:

    # =====================================================
    # MENSAJE DEL USUARIO
    # =====================================================

    st.session_state.messages.append({
        "role": "user",
        "content": pregunta
    })

    with st.chat_message(
        "user",
        avatar="🧑"
    ):

        st.markdown(pregunta)

    # =====================================================
    # RESPUESTA DE LA IA
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="⚡"
    ):

        try:

            with st.spinner("Pensando..."):

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

Si el usuario pregunta programación:

- explica paso a paso
- proporciona código funcional
- explica los errores
- evita complicar innecesariamente
  las soluciones

Si el usuario pide código:

- entrega código completo cuando
  sea necesario
- usa bloques de código
- explica dónde debe colocarlo

No inventes información.

Si no sabes algo,
dilo claramente.

Sé directo y evita respuestas
innecesariamente largas.
"""
                    }
                ]

                mensajes.extend(
                    st.session_state.messages
                )

                respuesta = client.chat.completions.create(
                    model=st.session_state.model,
                    messages=mensajes,
                    temperature=0.7,
                    max_tokens=2048
                )

                texto = respuesta.choices[0].message.content

                st.markdown(texto)

                # =========================================
                # GUARDAR RESPUESTA
                # =========================================

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
Santi IA ⚡ · Python + Streamlit + Groq
</div>
""", unsafe_allow_html=True)