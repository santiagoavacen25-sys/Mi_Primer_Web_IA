import streamlit as st

st.title("Mi primera pruebe manual")

nombre= st.text_input("Escribe tu juego favorito:")

if st.button("Mostrar juego"):
    st.write(f"Tu juego favorito es: {nombre}")
    