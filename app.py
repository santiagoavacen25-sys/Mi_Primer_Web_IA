import streamlit as st

# Configuración de la pestaña en el navegador
st.set_page_config(page_title="Mi Primera Web IA", page_icon="🚀", layout="centered")

# Barra lateral (Sidebar)
st.sidebar.title("⚙️ Panel de Control")
nombre = st.sidebar.text_input("¿Cómo te llamas?", "Santiago")
st.sidebar.write(f"¡Hola, {nombre}! 👋")

# Contenido principal
st.title("🚀 Mi Primera App Web con IA")
st.write("¡Bienvenido a mi sitio web interactivo publicado en internet!")

st.divider()

# Sección interactiva
st.subheader("💡 Interacción rápida")
mensaje = st.text_input("Escribe un mensaje para la app:", "¡Python y Streamlit están geniales!")

if st.button("Procesar mensaje"):
    st.success(f"Procesado con éxito: **{mensaje.upper()}**")
    st.balloons()  # ¡Efecto de globos en pantalla!