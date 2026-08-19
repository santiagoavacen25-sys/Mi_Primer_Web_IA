import streamlit as st
import ollama

# Configuración de la página
st.set_page_config(page_title="Mi Perfil & Asistente IA", page_icon="⚡", layout="centered")

# --- CABECERA Y PERFIL ---
st.markdown("<h1 style='text-align: center;'>⚡ ¡Hola, soy Santi!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Programador en Python | Proyectos Web & Gaming</p>", unsafe_allow_html=True)

st.divider()

# --- ENLACES RÁPIDOS ---
st.subheader("🌐 Mis Redes y Enlaces")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.link_button("💻 GitHub", "https://github.com", use_container_width=True)
with col_b:
    st.link_button("🎮 Discord", "https://discord.com", use_container_width=True)
with col_c:
    st.link_button("🎥 YouTube", "https://youtube.com", use_container_width=True)

st.divider()

# --- ASISTENTE VIRTUAL IA ---
st.subheader("🤖 Chatea con mi Asistente Virtual")
st.write("Pregúntale a mi IA sobre mis proyectos, mi setup, mis juegos o pedirle ayuda en Python.")

# Información base del asistente (System Prompt)
CONTEXTO_ASISTENTE = """
Eres el asistente virtual personal de Santi en su página web.
Responde de forma amable, clara y breve en español.
Aquí tienes los datos principales sobre Santi:
- Tiene 19 años.
- Le apasiona la programación con Python, el desarrollo de aplicaciones web y proyectos de IA.
- Sus proyectos principales incluyen una Calculadora Gamer y un Organizador de Metas y Tareas hecho en Streamlit.
- Juega títulos como Fortnite, Rocket League y Minecraft en PC y consola.
- Su equipo de desarrollo cuenta con almacenamiento SSD y tarjeta gráfica NVIDIA GTX 1050 Ti.
Si te preguntan sobre dudas de código en Python, responde con ejemplos sencillos y explicaciones claras.
"""

# Inicializar historial de chat en la memoria de la sesión
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

# Mostrar el historial de conversación en pantalla
for mensaje in st.session_state.historial_chat:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Entrada de texto para el usuario
if preg := st.chat_input("Escribe una pregunta para el asistente..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state.historial_chat.append({"role": "user", "content": preg})
    with st.chat_message("user"):
        st.markdown(preg)

    # Generar la respuesta usando el modelo liviano de Ollama en tu PC
    with st.chat_message("assistant"):
        with st.spinner("Pensando respuesta..."):
            try:
                              
                mensajes_para_ollama = [{"role": "system", "content": CONTEXTO_ASISTENTE}]
                for m in st.session_state.historial_chat:
                    mensajes_para_ollama.append({"role": m["role"], "content": m["content"]})
                
                respuesta_ollama = ollama.chat(
                    model='qwen2.5:1.5b',
                    messages=mensajes_para_ollama
                )
                
                texto_respuesta = respuesta_ollama['message']['content']
                st.markdown(texto_respuesta)
                
                # Guardar respuesta de la IA en la sesión
                st.session_state.historial_chat.append({"role": "assistant", "content": texto_respuesta})
                
            except Exception as e:
                st.error("No se pudo conectar con Ollama. Asegúrate de tener la app de Ollama ejecutándose.")


st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Sitio impulsado localmente con Python & Ollama 🐍</p>", unsafe_allow_html=True)