import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mi Perfil | Developer & Gamer", page_icon="⚡", layout="centered")

# --- CABECERA / PERFIL ---
st.markdown("<h1 style='text-align: center;'>⚡ ¡Hola, soy Santi!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Aprendiéndo a programar en Python | Gamer & Creador de Proyectos Web</p>", unsafe_allow_html=True)

st.divider()

# --- SECCIÓN DE PROYECTOS / SOBRE MÍ ---
st.subheader("🚀 Mis Proyectos")

col1, col2 = st.columns(2)

with col1:
    st.info("**🎯 Organizador de Metas**\n\nApp web interactiva para gestionar pendientes diarias, filtrar categorías y ver progreso en tiempo real.")

with col2:
    st.success("**🎮 Calculadora Gamer**\n\nHerramienta con métricas visuales y estadísticas para analizar horas de juego y rendimiento.")

st.divider()

# --- SECCIÓN DE ENLACES (LINKTREE) ---
st.subheader("🌐 Mis Redes y Enlaces")

# Botones que dirigen a tus perfiles
st.link_button("💻 Mi Perfil de GitHub", "https://github.com", use_container_width=True)
st.link_button("🎮 Miembros de mi Comunidad en Discord", "https://discord.com", use_container_width=True)
st.link_button("🎥 Canal / Stream", "https://youtube.com", use_container_width=True)

st.divider()

# --- SECCIÓN EXTRA: SETUP / HARDWARE ---
with st.expander("💻 Ver mi Setup de Programación y Gaming"):
    st.write("- **Procesador:** Intel / Apple Silicon")
    st.write("- **Gráfica:** NVIDIA GTX 1050 Ti / MX450")
    st.write("- **Almacenamiento:** 1 TB SSD")
    st.write("- **Software:** VS Code, Python, Streamlit, Git & GitHub Desktop")

st.markdown("<br><p style='text-align: center; font-size: 12px; color: gray;'>Construido desde cero con Python & Streamlit 🐍</p>", unsafe_allow_html=True)
    