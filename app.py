import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi Perfil & Asistente IA", page_icon="⚡")

st.title("⚡ ¡Hola, soy Santi!")
st.write("Programador en Python | Proyectos Web & Gaming")

# Botones de Redes
st.subheader("🌐 Mis Redes y Enlaces")
col1, col2, col3 = st.columns(3)
with col1:
    st.link_button("💻 GitHub", "https://github.com")
with col2:
    st.link_button("🎮 Discord", "https://discord.com")
with col3:
    st.link_button("🎥 YouTube", "https://youtube.com")

st.divider()

st.subheader("🤖 Chatea con mi Asistente Virtual")
st.caption("Pregúntale a mi IA sobre mis proyectos, mi setup, mis juegos o pedirle ayuda en Python.")

# Conexión con Groq usando Secrets de Streamlit Cloud
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

CONTEXTO_ASISTENTE = "Eres el asistente virtual personal de Santi. Responde brevemente en español."

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Historial de chat
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada de chat
if prompt := st.chat_input("Escribe una pregunta para el asistente..."):
    st.session_state.historial_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            mensajes_for_api = [{"role": "system", "content": CONTEXTO_ASISTENTE}] + st.session_state.historial_chat
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=mensajes_for_api
            )
            
            respuesta = completion.choices[0].message.content
            st.markdown(respuesta)
            st.session_state.historial_chat.append({"role": "assistant", "content": respuesta})
            
        except Exception as e:
            st.error("Hubo un error al conectar con la IA. Asegúrate de configurar la clave GROQ_API_KEY.")