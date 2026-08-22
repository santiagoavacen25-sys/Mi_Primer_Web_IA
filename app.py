import json
import os
import streamlit as st
from groq import Groq
                texto = respuesta.choices[0].message.content
                st.markdown(texto)

                # Guardar respuesta en la sesión
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": texto
                })

                # GUARDADO AUTOMÁTICO EN EL ARCHIVO JSON
                with open("chats_guardados.json", "w") as archivo:
                    json.dump(st.session_state.messages, archivo)

        except Exception as e:
            st.error("❌ Ocurrió un error al conectar con la IA.")
            st.code(str(e))

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
Santi IA ⚡ · Python + Streamlit + Groq
</div>
""", unsafe_allow_html=True)