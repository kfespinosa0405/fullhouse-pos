from services.ui_config import (
    ocultar_menu_streamlit
)

from pathlib import Path

import streamlit as st

from services.db import conectar


# ==================================
# CONFIGURACIÓN
# ==================================

st.set_page_config(
    page_title="FULL HOUSE POS",
    page_icon="🍽️",
    layout="wide"
)

ocultar_menu_streamlit()

# ==================================
# SESIÓN
# ==================================

if "logueado" not in st.session_state:
    st.session_state.logueado = False


# ==================================
# LOGIN
# ==================================

def validar(usuario, password):

    usuario = usuario.strip()
    password = password.strip()

    if not usuario:

        st.warning(
            "Ingrese un usuario"
        )

        return False

    if not password:

        st.warning(
            "Ingrese una contraseña"
        )

        return False

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario=?
            AND password=?
        """, (
            usuario,
            password
        ))

        resultado = cursor.fetchone()

        conn.close()

        if resultado:

            st.session_state.logueado = True
            st.session_state.usuario = usuario

            return True

        st.error(
            "Usuario o contraseña incorrectos"
        )

        return False

    except Exception as e:

        st.error(
            f"No fue posible iniciar sesión.\n\n{e}"
        )

        return False


# ==================================
# SI YA ESTÁ LOGUEADO
# ==================================

if st.session_state.logueado:

    st.switch_page(
        "pages/mapa_restaurante.py"
    )


# ==================================
# ESTILOS
# ==================================

st.markdown("""
<style>

div[data-testid="stButton"] button {

    height:75px;
    font-size:20px;
    font-weight:bold;

}

</style>
""", unsafe_allow_html=True)


# ==================================
# LOGO
# ==================================

logo = Path(
    "assets/logo_fullhouse.jpeg"
)

col1, col2, col3 = st.columns(
    [1, 2, 1]
)

with col2:

    if logo.exists():

        st.image(
            str(logo),
            use_container_width=True
        )

    else:

        st.markdown(
            "<h1 style='text-align:center'>FULL HOUSE</h1>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<h4 style='text-align:center;color:gray'>Sistema POS</h4>",
        unsafe_allow_html=True
    )

    usuario = st.text_input(
        "Usuario"
    )

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button(
        "INGRESAR",
        use_container_width=True
    ):

        if validar(
            usuario,
            password
        ):

            st.rerun()

    st.markdown(
        "<p style='text-align:center;color:gray'>FULL HOUSE POS v1.0</p>",
        unsafe_allow_html=True
    )