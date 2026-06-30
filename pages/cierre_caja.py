from services.ui_config import (
    ocultar_menu_streamlit
)

import streamlit as st
from datetime import datetime

from services.caja_service import (
    ventas_del_dia,
    total_del_dia
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
    page_title="Cierre de Caja",
    page_icon="💰",
    layout="wide"
)
ocultar_menu_streamlit()

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.image(
        "logo_fullhouse.jpeg",
        use_container_width=True
    )


    if st.button(
        "📍 Mapa Restaurante",
        use_container_width=True
    ):
        st.switch_page(
            "pages/mapa_restaurante.py"
        )

# ==================================
# CONTENIDO
# ==================================

st.title("📊 Cierre de Caja")

st.write(
    datetime.now().strftime(
        "%d/%m/%Y"
    )
)

st.divider()

ventas = ventas_del_dia()

if not ventas:

    st.info(
        "No existen ventas registradas hoy."
    )

else:

    total = 0

    for pedido_id, fecha, monto in ventas:

        col1, col2, col3 = st.columns(
            [1, 3, 1]
        )

        col1.write(
            f"#{pedido_id}"
        )

        col2.write(
            fecha
        )

        col3.write(
            f"${monto:.2f}"
        )

        total += monto

    st.divider()

    st.metric(
        "TOTAL DEL DÍA",
        f"${total:.2f}"
    )
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "📄 Descargar PDF",
            use_container_width=True,
            key="btn_pdf"
        )
    with col2:
        if st.button(
            "❌ Cerrar Caja",
            use_container_width=True,
            key="btn_cerrar"
        ):
    st.success("Caja cerrada correctamente.")

