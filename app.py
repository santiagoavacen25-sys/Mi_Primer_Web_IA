import streamlit as st

st.set_page_config(page_title="Gestor de Perfiles", page_icon="🎮")

st.title("🎮 Registro de Jugadores")

# Inicializar la lista de diccionarios
if "jugadores" not in st.session_state:
    st.session_state["jugadores"] = []

# Formulario para capturar varios datos a la vez
with st.form("formulario_jugador"):
    nombre = st.text_input("Nombre de usuario:")
    juego = st.selectbox("Juego favorito:", ["Fortnite", "Rocket League", "Minecraft", "Roblox"])
    plataforma = st.radio("Plataforma:", ["PC", "PlayStation 5", "Otro"])
    
    enviado = st.form_submit_button("Guardar Registro")

if enviado:
    if nombre.strip() != "":
        # Creamos un DICCIONARIO con todos los datos
        nuevo_jugador = {
            "nombre": nombre,
            "juego": juego,
            "plataforma": plataforma
        }
        # Guardamos el diccionario dentro de la lista
        st.session_state["jugadores"].append(nuevo_jugador)
        st.success(f"¡Perfil de {nombre} registrado!")
    else:
        st.warning("Escribe un nombre de usuario.")

st.divider()

# Mostrar la lista de diccionarios
st.subheader("📋 Lista de Registrados:")

if len(st.session_state["jugadores"]) > 0:
    for i, p in enumerate(st.session_state["jugadores"], 1):
        # Accedemos a los valores usando las claves del diccionario: p["clave"]
        st.write(f"**{i}. {p['nombre']}** — Juega a *{p['juego']}* en *{p['plataforma']}*")
else:
    st.info("No hay ningún jugador registrado aún.")

if st.button("Borrar todos los registros"):
    st.session_state["jugadores"] = []
    st.rerun()