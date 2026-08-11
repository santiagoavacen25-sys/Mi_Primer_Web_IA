import streamlit as st

st.set_page_config(page_title="Gestor de Perfiles", page_icon="🎮", layout="centered")

st.title("🎮 Registro de Jugadores")

# Inicializar la lista
if "jugadores" not in st.session_state:
    st.session_state["jugadores"] = []

# --- PANEL DE MÉTRICAS / ESTADÍSTICAS ---
st.subheader("📊 Estadísticas en vivo")

total = len(st.session_state["jugadores"])
pc_count = sum(1 for p in st.session_state["jugadores"] if p["plataforma"] == "PC")
ps5_count = sum(1 for p in st.session_state["jugadores"] if p["plataforma"] == "PlayStation 5")

col1, col2, col3 = st.columns(3)
col1.metric("Total Jugadores", total)
col2.metric("En PC 💻", pc_count)
col3.metric("En PS5 🎮", ps5_count)

st.divider()

# --- FORMULARIO DE REGISTRO ---
with st.form("formulario_jugador"):
    nombre = st.text_input("Nombre de usuario:")
    juego = st.selectbox("Juego favorito:", ["Fortnite", "Rocket League", "Minecraft", "Roblox"])
    plataforma = st.radio("Plataforma:", ["PC", "PlayStation 5", "Otro"])
    
    enviado = st.form_submit_button("Guardar Registro")

if enviado:
    if nombre.strip() != "":
        nuevo_jugador = {
            "nombre": nombre,
            "juego": juego,
            "plataforma": plataforma
        }
        st.session_state["jugadores"].append(nuevo_jugador)
        st.success(f"¡Perfil de {nombre} registrado!")
        st.rerun()  # Actualiza los contadores de arriba al instante
    else:
        st.warning("Escribe un nombre de usuario.")

# --- LISTA DE REGISTRADOS ---
st.subheader("📋 Lista de Registrados:")

if total > 0:
    for i, p in enumerate(st.session_state["jugadores"], 1):
        st.write(f"**{i}. {p['nombre']}** — Juega a *{p['juego']}* en *{p['plataforma']}*")
else:
    st.info("No hay ningún jugador registrado aún.")

if st.button("Borrar todos los registros"):
    st.session_state["jugadores"] = []
    st.rerun()