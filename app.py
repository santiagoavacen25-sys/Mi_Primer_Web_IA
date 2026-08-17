import streamlit as st

st.set_page_config(page_title="Calculadora Gamer", page_icon="🎮")

st.title("🎮 Calculadora de Horas de Juego")

# 1. CREAR MEMORIA (Si no existe todavía)
if "historial" not in st.session_state:
    st.session_state.historial = []

# 2. ENTRADAS DE DATOS
juego = st.text_input("¿Qué juego estás jugando actualmente?")
pais = st.text_input("¿De qué país eres?")
plataforma = st.selectbox("Selecciona tu plataforma principal:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])
horas_diarias = st.slider("¿Cuántas horas juegas al día aproximadamente?", min_value=1, max_value=12, value=2)

# 3. BOTÓN Y REGISTRO EN MEMORIA
if st.button("Calcular y guardar estadísticas"):
    horas_semanales = horas_diarias * 7
    
    # Guardamos este registro en la lista dentro de la memoria
    nuevo_registro = f"🎮 {juego} ({plataforma}) - {horas_semanales} hrs/semana [{pais}]"
    st.session_state.historial.append(nuevo_registro)

# 4. MOSTRAR EL HISTORIAL GUARDADO
if st.session_state.historial:
    st.divider()
    st.subheader("📜 Historial de Juegos Guardados:")
    for item in st.session_state.historial:
        st.write(item)