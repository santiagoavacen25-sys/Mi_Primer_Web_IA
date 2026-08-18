import streamlit as st
import ollama

st.set_page_config(page_title="Mi Agente Personal", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Asistente Agéntico Personal")

# Instrucción de sistema (Define el rol y personalidad del Agente)
SYSTEM_PROMPT = """
Eres un Agente de IA Personal especializado en productividad y desarrollo en Python.
Tus responsabilidades:
1. Responder de forma estructurada, técnica y directa.
2. Si el usuario te pide un código, entrégalo optimizado y limpio.
3. Ayudar al usuario a planificar proyectos de software paso a paso.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Mostrar chat omitiendo el mensaje interno de sistema
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Pídele algo a tu Agente (ej: 'Planifica mi app en 3 pasos')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("El Agente está procesando la tarea..."):
            response = ollama.chat(
                model="qwen2.5-coder:1.5b",
                messages=st.session_state.messages
            )
            answer = response["message"]["content"]
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})