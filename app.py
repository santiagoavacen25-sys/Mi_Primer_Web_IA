import streamlit as st

# Configuración básica de la página
st.set_page_config(page_title="Calculadora Gamer", page_icon="🎮")

st.title("🎮 Calculadora de Horas de Juego")
st.write("Escribe tus datos para calcular cuántas horas juegas a la semana.")

# 1. ENTRADAS DE DATOS (Variables)
juego = st.text_input("¿Qué juego estás jugando actualmente?")
plataforma = st.selectbox("Selecciona tu plataforma principal:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])
horas_diarias = st.slider("¿Cuántas horas juegas al día aproximadamente?", min_value=1, max_value=12, value=2)

# 2. BOTÓN DE ACCIÓN Y LÓGICA
if st.button("Calcular estadísticas"):
    # Cálculo matemático sencillo
    horas_semanales = horas_diarias * 7
    
    st.divider()
    st.subheader("📊 Tus Resultados:")
    st.write(f"Juegas **{juego}** en **{plataforma}**.")
    st.write(f"A la semana acumulas aproximadamente **{horas_semanales} horas** de juego.")
    
    # Condicionales para reaccionar a las horas
    if horas_semanales <= 10:
        st.info("🌱 Jugador casual: Buen equilibrio entre el juego y tus otras actividades.")
    elif horas_semanales <= 25:
        st.success("⚡ Jugador dedicado: ¡Le dedicas buen tiempo a subir de nivel!")
    else:
        st.warning("🔥 ¡Modo Tryhard!: Llevas bastantes horas en pantalla, recuerda hacer pausas para descansar los ojos.")

    # Reacción según la plataforma
    if plataforma == "PC":
        st.caption("💻 Configuración optimizada para máximo rendimiento.")
    else:
        st.caption("🎮 Modo cómodo desde la consola.")
