import streamlit as st

st.set_page_config(page_title="Mi Organizador Gamer", page_icon="🎯")

st.title("🎯 Mi Panel de Metas y Tareas")
st.write("Organiza tus pendientes de juego, proyectos de código y tareas diarias.")

# 1. INICIALIZAR MEMORIA (LISTA DE TAREAS)
if "tareas" not in st.session_state:
    st.session_state.tareas = []

# 2. BARRA LATERAL PARA AGREGAR TAREAS
st.sidebar.header("➕ Agregar Nueva Tarea")
nueva_tarea = st.sidebar.text_input("Escribe tu pendiente o meta:")
categoria = st.sidebar.selectbox("Categoría:", ["🎮 Juegos", "💻 Programación", "📚 Personal"])

if st.sidebar.button("Guardar Tarea"):
    if nueva_tarea.strip() != "":
        # Guardamos la tarea como un diccionario (texto, categoría y estado)
        item = {"texto": nueva_tarea, "categoria": categoria, "completada": False}
        st.session_state.tareas.append(item)
        st.sidebar.success("¡Tarea agregada!")
        st.rerun()

# 3. MOSTRAR TAREAS EN LA PANTALLA PRINCIPAL
if st.session_state.tareas:
    st.subheader("📋 Tu Lista de Pendientes:")
    
    for idx, tarea in enumerate(st.session_state.tareas):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**[{tarea['categoria']}]** {tarea['texto']}")
        with col2:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.tareas.pop(idx)
                st.rerun()
else:
    st.info("Aún no tienes tareas guardadas. Agrega una desde la barra lateral. 👈")
    st.info("Aún no tienes tareas guardadas. Agrega una desde la barra lateral. 👈")