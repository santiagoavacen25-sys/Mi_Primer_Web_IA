import streamlit as st

st.set_page_config(page_title="Calculadora Gamer", page_icon="🎮")

st.title("🎮 Calculadora de Horas de Juego")

# 1. MEMORIA DEL SISTEMA
if "historial" not in st.session_state:
    st.session_state.historial = []
if "horas_lista" not in st.session_state:
    st.session_state.horas_lista = []

# 2. BARRA LATERAL
st.sidebar.header("⚙️ Configuración")
juego = st.sidebar.text_input("¿Qué juego estás jugando actualmente?")
pais = st.sidebar.text_input("¿De qué país eres?")
plataforma = st.sidebar.selectbox("Plataforma principal:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])
horas_diarias = st.sidebar.slider("Horas jugadas al día:", min_value=1, max_value=12, value=2)

# 3. BOTÓN PRINCIPAL Y MÉTRICAS
if st.button("Calcular y guardar estadísticas"):
    horas_semanales = horas_diarias * 7
    
    # Guardar en las dos listas de memoria
    nuevo_registro = f"🎮 {juego} ({plataforma}) - {horas_semanales} hrs/semana [{pais}]"
    st.session_state.historial.append(nuevo_registro)
    st.session_state.horas_lista.append(horas_semanales)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Juego Actual", value=juego if juego else "Sin nombre")
    with col2:
        st.metric(label="Horas Semanales", value=f"{horas_semanales} hrs")

# 4. GRÁFICO DE BARRAS E HISTORIAL
if st.session_state.historial:
    st.divider()
    
    # Muestra del gráfico interactivo
    st.subheader("📊 Gráfico de Horas Semanales Por Registro:")
    st.bar_chart(st.session_state.horas_lista)
    
    st.subheader("📜 Historial de Juegos Guardados:")
    for item in st.session_state.historial:
        st.write(item)
        
    if st.button("🗑️ Limpiar historial"):
        st.session_state.historial = []
        st.session_state.horas_lista = []
        st.rerun()