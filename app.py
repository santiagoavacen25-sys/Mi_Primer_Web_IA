import streamlit as st

st.title("Mi primera prueba manual")

nombre = st.text_input("Escribe tu juego favorito:")
# Cambiamos st.text_input por st.selectbox
plataforma = st.selectbox("Selecciona tu plataforma:", ["PC", "PlayStation 5", "Xbox", "Nintendo Switch"])

if st.button("Mostrar juego"):
    st.write(f"Juegas {nombre} en {plataforma}")
    
