import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi Perfil & Asistente IA", page_icon="⚡")

st.title("⚡ ¡Hola, soy Santi!")
st.write("Programador en Python | Proyectos Web & Gaming")

# Conexión con Groq usando Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

CONTEXTO_ASISTENTE = "Eres el asistente virtual personal de Santi. Responde brevemente en español."

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Dibujar historial
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada de chat
if prompt := st.chat_input("Escribe una pregunta para el asistente..."):
    # Mostrar mensaje del usuario
    st.session_state.historial_chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        try:
            mensajes_for_api = [{"role": "system", "content": CONTEXTO_ASISTENTE}] + st.session_state.historial_chat

            completion = client.chat.completions.create(
              model="llama-3.1-8b-instant",
                messages=mensajes_for_api
            )

            respuesta = completion.choices[0].message.content
            st.markdown(respuesta)
            st.session_state.historial_chat.append({"role": "assistant", "content": respuesta})

        except Exception as e:
            st.error(f"Error detallado: {e}")