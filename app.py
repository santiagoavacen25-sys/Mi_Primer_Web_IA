import streamlit as st

# 1. Título principal con un emoji genial
st.title("🤖 Mi Primera Web Inteligente")

# 2. Un texto de bienvenida
st.write("¡Hola! Esta es una página web real interactiva creada desde cero.")

# 3. La caja de texto mágica (guarda lo que el usuario escribe)
nombre = st.text_input("Introduce tu nombre para iniciar el sistema:")

# 4. Un condicional: SI el usuario escribe su nombre, pasan cosas
if nombre:
    st.success(f"¡Acceso concedido, {nombre}! 🚀")
    
    # Agregamos un botón interactivo
    if st.button("Haz clic aquí para ver una sorpresa"):
        st.balloons()  # ¡Esto va a lanzar una animación en toda tu pantalla!
        st.write("¡Boom! Acabas de activar una función web con solo un clic.")