import streamlit as st

st.set_page_config(
    page_title="FULL HOUSE POS",
    page_icon="🍽️"
)

if st.session_state.get("logueado", False):
    st.switch_page("pages/mapa_restaurante.py")

st.title("FULL HOUSE POS")

usuario = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

if st.button("Ingresar", use_container_width=True):

    # TODO: reemplazar por tu servicio real de login
    if usuario and password:

        st.session_state["logueado"] = True

        st.switch_page(
            "pages/mapa_restaurante.py"
        )

    else:

        st.error(
            "Ingrese usuario y contraseña."
        )
