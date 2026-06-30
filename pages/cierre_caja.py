from services.ui_config import ocultar_menu_streamlit

import streamlit as st
from datetime import datetime

from services.caja_service import (
    ventas_del_dia,
    total_del_dia
)

# ==================================
# SEGURIDAD
# ==================================

if not st.session_state.get("logueado", False):
    st.switch_page("streamlit_app.py")

# ==================================
# ESTILOS
# ==================================

ocultar_menu_streamlit()

# ==================================
# MENÚ LATERAL
# ==================================

with st.sidebar:

    st.image(
        "logo_fullhouse.jpeg",
        use_container_width=True
    )

    st.markdown("## FULL HOUSE POS")

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

st.write(datetime.now().strftime("%d/%m/%Y"))

st.divider()

ventas = ventas_del_dia()

if not ventas:

    st.info("No existen ventas registradas hoy.")

else:

    total = 0

    st.subheader("Ventas del día")

    cab1, cab2, cab3 = st.columns([1,3,1])

    cab1.markdown("**Pedido**")
    cab2.markdown("**Fecha / Hora**")
    cab3.markdown("**Total**")

    st.divider()

    for pedido_id, fecha, monto in ventas:

        c1, c2, c3 = st.columns([1,3,1])

        c1.write(f"#{pedido_id}")
        c2.write(fecha)
        c3.write(f"${monto:.2f}")

        total += monto

    st.divider()

    st.metric(
        "TOTAL DEL DÍA",
        f"${total:.2f}"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📄 Descargar PDF",
            use_container_width=True,
            type="primary"
        ):
            st.info("Aquí generaremos el PDF del cierre de caja.")

    with col2:

        if st.button(
            "❌ Cerrar Caja",
            use_container_width=True
        ):
            st.success("Caja cerrada correctamente.")
