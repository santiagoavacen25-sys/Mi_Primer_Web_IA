import streamlit as st

st.title("Mi primera prueba manual")

nombre = st.text_input("Escribe tu juego favorito:")
plataforma = st.selectbox("Selecciona tu plataforma:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])

if st.button("Mostrar juego"):
    st.write(f"Juegas {nombre} en {plataforma}")
    
    if plataforma == "PC":
        st.success("¡Master Race! Buena elección de plataforma.")
    else:
        st.info("¡Buena plataforma de consola para jugar cómodo!")
    
