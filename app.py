import streamlit as st
from groq import Groq

# =========================================================
# CONFIGURACIÓN
# =========================================================

col1 ,col2, col3=st.columns([1, 1, 1])

with col2:
    st.image("Gemini_Generated_Image_olxfs4olxfs4olxf.jpeg", width=150)
    

st.set_page_config(
    page_title="Santi AI ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILOS
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
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

/* =========================================================
   HEADER
   ========================================================= */

.hero {
    text-align: center;
    padding: 35px 20px 25px 20px;
}

.logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 70px;
    height: 70px;
    border-radius: 22px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    font-size: 34px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}

.hero h1 {
    font-size: 42px;
    margin: 18px 0 8px 0;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero p {
    color: #aeb6cc;
    font-size: 16px;
}

/* =========================================================
   TARJETAS
   ========================================================= */

.glass {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 22px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.18);
}

/* =========================================================
   BOTONES
   ========================================================= */

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

/* =========================================================
   CHAT
   ========================================================= */

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    margin-bottom: 10px;
}

/* =========================================================
   INPUT
   ========================================================= */

[data-testid="stChatInput"] {
    border-radius: 18px;
}

/* =========================================================
   SELECT
   ========================================================= */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
}

/* =========================================================
   FOOTER
   ========================================================= */

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
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
<div class="logo">⚡</div>
<h1>Santi IA</h1>
<p>Tu asistente de inteligencia artificial para aprender, programar, crear y resolver problemas.</p>
</div>
""", unsafe_allow_html=True)


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

    # 1. BUCLE FOR PARA MOSTRAR LOS CHATS
    for nombre_chat in list(st.session_state.chats):
        if st.button(f"💬 {nombre_chat}"):
         st.session_state.messages = st.session_state.chats[nombre_chat]
         st.rerun() 
          
  # 2. Botón para ELIMINAR solo este chat
             
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