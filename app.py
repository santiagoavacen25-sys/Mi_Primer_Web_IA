import streamlit as st

st.set_page_config(page_title="Calculadora Gamer", page_icon="🎮")

st.title("🎮 Calculadora de Horas de Juego")

# Memoria del sistema
if "historial" not in st.session_state:
    st.session_state.historial = []

# BARRA LATERAL (Sidebar)
st.sidebar.header("⚙️ Configuración")
juego = st.sidebar.text_input("¿Qué juego estás jugando actualmente?")
pais = st.sidebar.text_input("¿De qué país eres?")
plataforma = st.sidebar.selectbox("Plataforma principal:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])
horas_diarias = st.sidebar.slider("Horas jugadas al día:", min_value=1, max_value=12, value=2)

# Botón principal en el centro
if st.button("Calcular y guardar estadísticas"):
    horas_semanales = horas_diarias * 7
    nuevo_registro = f"🎮 {juego} ({plataforma}) - {horas_semanales} hrs/semana [{pais}]"
    st.session_state.historial.append(nuevo_registro)

# Muestra del historial
if st.session_state.historial:
    st.divider()
    st.subheader("📜 Historial de Juegos Guardados:")
    for item in st.session_state.historial:
        st.write(item)
        
    if st.button("🗑️ Limpiar historial"):
        st.session_state.historial = []
        st.rerun()
