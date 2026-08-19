import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi Perfil & Asistente IA", page_icon="⚡")

st.title("⚡ ¡Hola, soy Santi!")
st.write("Programador en Python | Proyectos Web & Gaming")

# Conexión con Groq usando la clave guardada en Secrets
client = Groq(
    api_key="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"
)

CONTEXTO_ASISTENTE = "Eres el asistente virtual personal de Santi. Responde brevemente en español."

if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Dibujar historial
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada de chat
if preg := st.chat_input("Escribe una pregunta para el asistente..."):
    st.session_state.historial_chat.append({"role": "user", "content": preg})
    with st.chat_message("user"):
        st.markdown(preg)

    with st.chat_message("assistant"):
        with st.spinner("Pensando respuesta..."):
            try:
                mensajes_para_ia = [{"role": "system", "content": CONTEXTO_ASISTENTE}]
                for m in st.session_state.historial_chat:
                    mensajes_para_ia.append({"role": m["role"], "content": m["content"]})
                
                # Respuesta de la IA en la nube
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=mensajes_para_ia,
                )
                
                texto_respuesta = response.choices[0].message.content
                st.markdown(texto_respuesta)
                st.session_state.historial_chat.append({"role": "assistant", "content": texto_respuesta})
                
            except Exception as e:
                st.error("Hubo un error al conectar con la IA. Asegúrate de configurar la clave GROQ_API_KEY.") 