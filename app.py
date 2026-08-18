import streamlit as st

st.set_page_config(page_title="Mi Organizador Gamer", page_icon="🎯")

st.title("🎯 Mi Panel de Metas y Tareas")
st.write("Organiza tus pendientes de juego, proyectos de código y tareas diarias.")

# 1. INICIALIZAR MEMORIA
if "tareas" not in st.session_state:
    st.session_state.tareas = []

# 2. BARRA LATERAL PARA AGREGAR TAREAS
st.sidebar.header("➕ Agregar Nueva Tarea")
nueva_tarea = st.sidebar.text_input("Escribe tu pendiente o meta:")
categoria = st.sidebar.selectbox("Categoría:", ["🎮 Juegos", "💻 Programación", "📚 Personal"])

if st.sidebar.button("Guardar Tarea"):
    if nueva_tarea.strip() != "":
        item = {"texto": nueva_tarea, "categoria": categoria, "completada": False}
        st.session_state.tareas.append(item)
        st.sidebar.success("¡Tarea agregada!")
        st.rerun()

# 3. BARRA DE PROGRESO Y MOSTRAR TAREAS
if st.session_state.tareas:
    # Cálculo de tareas completadas
    total_tareas = len(st.session_state.tareas)
    completadas = sum(1 for t in st.session_state.tareas if t["completada"])
    porcentaje = completadas / total_tareas
    
    st.write(f"**Progreso actual:** {completadas} de {total_tareas} tareas completadas")
    st.progress(porcentaje)
    
    st.divider()
    st.subheader("📋 Tu Lista de Pendientes:")
    
    for idx, tarea in enumerate(st.session_state.tareas):
        col1, col2 = st.columns([4, 1])
        with col1:
            # Checkbox para marcar como completada
            check = st.checkbox(
                f"**[{tarea['categoria']}]** {tarea['texto']}", 
                value=tarea["completada"], 
                key=f"check_{idx}"
            )
            # Actualizamos el estado si cambia el checkbox
            st.session_state.tareas[idx]["completada"] = check
            
        with col2:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.tareas.pop(idx)
                st.rerun()
else:
    st.info("Aún no tienes tareas guardadas. Agrega una desde la barra lateral. 👈")
    