from services.ui_config import (
    ocultar_menu_streamlit
)

import streamlit as st

from services.estado_mesas_service import liberar_mesa
from services.mesas_service import cambiar_estado
from services.pedidos_service import cerrar_pedido


# ==================================
# SEGURIDAD
# ==================================

if not st.session_state.get("logueado", False):
    st.switch_page("streamlit_app.py")

if "pedido_id" not in st.session_state:
    st.error("No existe un pedido para cobrar.")
    st.stop()


# ==================================
# DATOS
# ==================================

pedido_id = st.session_state["pedido_id"]
nombre_mesa = st.session_state["mesa_actual"]
total = st.session_state["total_cobro"]


# ==================================
# CONFIG
# ==================================

st.set_page_config(
    page_title="Cobro",
    layout="centered"
)

ocultar_menu_streamlit()

with st.sidebar:

    st.title(
        "FULL HOUSE POS"
    )

    if st.button(
        "📍 Mapa Restaurante",
        use_container_width=True
    ):
        st.switch_page(
            "pages/mapa_restaurante.py"
        )

    if st.button(
        "📊 Cierre de Caja",
        use_container_width=True
    ):
        st.switch_page(
            "pages/cierre_caja.py"
        )

# ==================================
# FUNCIÓN FINALIZAR
# ==================================

def finalizar_venta():
    cerrar_pedido(pedido_id)

    liberar_mesa(nombre_mesa)

    cambiar_estado(
        nombre_mesa,
        "LIBRE"
    )

    st.session_state.pop("pedido_id", None)
    st.session_state.pop("total_cobro", None)
    st.session_state.pop("mesa_actual", None)

    st.success(
        "Venta finalizada correctamente."
    )

    st.switch_page(
        "pages/mapa_restaurante.py"
    )


# ==================================
# TÍTULO
# ==================================

st.title("Cobro de Cuenta")

st.divider()


# ==================================
# INFORMACIÓN
# ==================================

st.subheader(
    f"Mesa: {nombre_mesa}"
)

st.metric(
    "Total a cobrar",
    f"${total:.2f}"
)


# ==================================
# PAGO
# ==================================

recibido = st.number_input(
    "Valor recibido",
    min_value=0.0,
    step=1.0,
    format="%.2f"
)

cambio = recibido - total

if recibido > 0:
    st.metric(
        "Cambio",
        f"${cambio:.2f}"
    )


# ==================================
# BOTONES
# ==================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Finalizar Venta",
        use_container_width=True
    ):

        if recibido < total:

            st.error(
                "El valor recibido es menor al total."
            )

        else:

            finalizar_venta()

with col2:

    if st.button(
        "Cancelar",
        use_container_width=True
    ):

        st.switch_page(
            "pages/pedido.py"
        )
