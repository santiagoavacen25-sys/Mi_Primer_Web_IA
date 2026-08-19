import streamlit as st
from groq import Groq

# Configuración de página de Streamlit
st.set_page_config(page_title="Santiago | Perfil & IA", page_icon="⚡", layout="centered")

# --- ESTILOS CSS PERSONALIZADOS (Tu diseño HTML) ---
st.markdown("""
    <style>
    /* Estilos globales y contenedor */
    .main {
        background-color: #f0f8ff;
    }
    .header-box {
        background-color: #333333;
        color: #f0f8ff;
        padding: 20px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .header-box h1 {
        margin: 0;
        color: #f0f8ff;
    }
    .footer-box {
        background-color: #333333;
        color: #f0f8ff;
        padding: 15px;
        text-align: center;
        font-size: 14px;
        border-radius: 8px;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA (Header HTML) ---
st.markdown("""
    <div class="header-box">
        <h1>Santiago</h1>
        <p style="font-size: 16px; margin-top: 5px;">Programador en Python | Proyectos Web & Gaming</p>
    </div>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON GROQ ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
CONTEXTO_ASISTENTE = "Eres el asistente virtual personal de Santiago. Responde de forma breve, amable y directa en español."

# --- HISTORIAL DEL CHAT ---
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Dibujar mensajes guardados
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# --- ENTRADA DE CHAT E INTEGRACIÓN CON IA ---
if prompt := st.chat_input("Escribe una pregunta para el asistente..."):
    # Guardar y mostrar mensaje del usuario
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

# --- PIE DE PÁGINA (Footer HTML) ---
st.markdown("""
    <div class="footer-box">
        <p style="margin: 0;">Copyright © 2026 Santiago — Todos los derechos reservados</p>
    </div>
""", unsafe_allow_html=True)