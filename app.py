import streamlit as st

st.set_page_config(page_title="Mi Organizador Gamer", page_icon="🎯")

st.title("🎯 Mi Panel de Metas y Tareas")
st.write("Organiza tus pendientes de juego, proyectos de código y tareas diarias.")

# 1. INICIALIZAR MEMORIA
if "tareas" not in st.session_state:
    st.session_state.tareas = []

# 2. BARRA LATERAL PARA AGREGAR TAREAS Y FILTRAR
st.sidebar.header("➕ Agregar Nueva Tarea")
nueva_tarea = st.sidebar.text_input("Escribe tu pendiente o meta:")
categoria = st.sidebar.selectbox("Categoría:", ["🎮 Juegos", "💻 Programación", "📚 Personal"])

if st.sidebar.button("Guardar Tarea"):
    if nueva_tarea.strip() != "":
        item = {"texto": nueva_tarea, "categoria": categoria, "completada": False}
        st.session_state.tareas.append(item)
        st.sidebar.success("¡Tarea agregada!")
        st.rerun()

st.sidebar.divider()
st.sidebar.header("🔍 Filtro")
filtro_cat = st.sidebar.radio("Ver categoría:", ["Todas", "🎮 Juegos", "💻 Programación", "📚 Personal"])

# 3. BARRA DE PROGRESO Y MOSTRAR TAREAS
if st.session_state.tareas:
    total_tareas = len(st.session_state.tareas)
    completadas = sum(1 for t in st.session_state.tareas if t["completada"])
    porcentaje = completadas / total_tareas if total_tareas > 0 else 0.0
    
    st.write(f"**Progreso general:** {completadas} de {total_tareas} tareas completadas")
    st.progress(porcentaje)
    
    # Mensaje especial si logras el 100%
    if completadas == total_tareas and total_tareas > 0:
        st.balloons()
        st.success("🎉 ¡Felicidades! Has completado todas tus metas acumuladas.")
    
    st.divider()
    st.subheader("📋 Tu Lista de Pendientes:")
    
    for idx, tarea in enumerate(st.session_state.tareas):
        # Aplicamos el filtro de categoría seleccionada
        if filtro_cat == "Todas" or tarea["categoria"] == filtro_cat:
            col1, col2 = st.columns([4, 1])
            with col1:
                estado = st.checkbox(
                    f"**[{tarea['categoria']}]** {tarea['texto']}", 
                    value=tarea["completada"], 
                    key=f"check_{idx}"
                )
                if estado != tarea["completada"]:
                    st.session_state.tareas[idx]["completada"] = estado
                    st.rerun()
                
            with col2:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.tareas.pop(idx)
                    st.rerun()
else:
    st.info("Aún no tienes tareas guardadas. Agrega una desde la barra lateral. 👈")
    