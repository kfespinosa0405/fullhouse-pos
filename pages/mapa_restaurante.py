from services.ui_config import (
    ocultar_menu_streamlit
)

import streamlit as st

from services.mesas_service import (
    obtener_estado
)


# ==================================
# SEGURIDAD
# ==================================

if not st.session_state.get(
    "logueado",
    False
):
    st.switch_page(
        "streamlit_app.py"
    )


# ==================================
# CONFIG
# ==================================

st.set_page_config(
    page_title="FULL HOUSE POS",
    page_icon="🍽️",
    layout="wide"
)

ocultar_menu_streamlit()

# ==================================
# OCULTAR NAVEGACIÓN STREAMLIT
# ==================================

st.markdown("""
<style>

[data-testid="stSidebarNav"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)


# ==================================
# ESTADO MESA
# ==================================

def color_mesa(nombre):

    estado = obtener_estado(
        nombre
    )

    if estado == "OCUPADA":
        return "🔴"

    if estado == "CUENTA":
        return "🟠"

    return "🟢"


# ==================================
# ABRIR PEDIDO
# ==================================

def abrir_pedido(nombre):

    st.session_state["mesa_actual"] = nombre

    st.switch_page(
        "pages/pedido.py"
    )


# ==================================
# TÍTULO
# ==================================

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.markdown("""
    <h1 style='
    text-align:center;
    color:white;
    margin-bottom:0;
    '>
    FULL HOUSE
    </h1>

    <p style='
    text-align:center;
    color:#ff0000;
    letter-spacing:4px;
    '>
    FOOD • DRINKS • VIBES
    </p>
    """, unsafe_allow_html=True)



    if st.button(
        "📍 Mapa Restaurante",
        use_container_width=True
    ):
        st.rerun()

    if st.button(
        "📊 Cierre de Caja",
        use_container_width=True
    ):
        st.switch_page(
            "pages/cierre_caja.py"
        )

st.title(
    "FULL HOUSE POS"
)

st.subheader(
    "Mapa del Restaurante"
)

st.divider()


# ==================================
# DISTRIBUCIÓN ORIGINAL
# ==================================

filas = [

    ["A9", "A8", None, None, None, None, "VIP1", "VIP3"],

    ["A1", "A2", None, "A7", None, None, "VIP2", "VIP4"],

    [None, "A3", None, None, "A10", None, None, "VIP5"],

    [None, "A4", None, None, "A11", "A14"],

    ["A6", "A5", None, "A12", None, "A15"],

    [None, None, None, "A13"],

    [None, None, "A21", "A20", "A19", "A18", "A17", "A16"]
]


# ==================================
# PINTAR MAPA
# ==================================

for fila in filas:

    columnas = st.columns(
        len(fila)
    )

    for i, mesa in enumerate(fila):

        with columnas[i]:

            if mesa:

                estado = color_mesa(
                    mesa
                )

                if st.button(
                    f"{estado} {mesa}",
                    use_container_width=True,
                    key=mesa
                ):

                    abrir_pedido(
                        mesa
                    )


# ==================================
# REFRESH
# ==================================

if st.button(
    "Actualizar Estado de Mesas"
):

    st.rerun()