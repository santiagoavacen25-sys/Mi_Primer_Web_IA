import streamlit as st

st.set_page_config(page_title="App con Listas", page_icon="📋")

st.title("📋 Registro de Tareas o Historial")

# Inicializamos una lista en la memoria de la sesión si no existe
if "lista_datos" not in st.session_state:
    st.session_state["lista_datos"] = []

# Entrada de datos
nuevo_item = st.text_input("Escribe un elemento para agregar a la lista:")

if st.button("Guardar en la lista"):
    if nuevo_item.strip() != "":
        # Agregamos el elemento a la lista
        st.session_state["lista_datos"].append(nuevo_item)
        st.success(f"'{nuevo_item}' agregado correctamente.")
    else:
        st.warning("Escribe algo antes de guardar.")

st.divider()

# Mostrar la lista en pantalla
st.subheader("📜 Elementos guardados:")

if len(st.session_state["lista_datos"]) > 0:
    for i, item in enumerate(st.session_state["lista_datos"], 1):
        st.write(f"**{i}.** {item}")
else:
    st.info("La lista está vacía actualmente.")

# Botón para limpiar
if st.button("Limpiar lista"):
    st.session_state["lista_datos"] = []
    st.rerun()