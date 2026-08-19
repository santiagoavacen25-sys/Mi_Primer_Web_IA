import streamlit as st
import requests

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

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Historial de chat
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada de chat para Ollama local
if prompt := st.chat_input("Escribe una pregunta para el asistente..."):
    st.session_state.historial_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Petición a la API local de Ollama (puerto 11434)
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            respuesta = response.json()["response"]
            st.markdown(respuesta)
            st.session_state.historial_chat.append({"role": "assistant", "content": respuesta})
        except Exception as e:
            st.error("Asegúrate de que Ollama esté corriendo en tu sistema (`ollama run llama3.1:8b`).")