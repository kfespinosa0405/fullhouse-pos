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
# CONFIG
# ==================================

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

st.write(datetime.now().strftime("%d/%m/%Y"))

st.divider()

ventas = ventas_del_dia()

total = 0

if not ventas:

    st.info("No existen ventas registradas hoy.")

else:

    encabezado = st.columns([1,3,1])

    encabezado[0].markdown("**Pedido**")
    encabezado[1].markdown("**Fecha**")
    encabezado[2].markdown("**Total**")

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

st.divider()

st.subheader("Opciones")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "📄 Descargar PDF",
        use_container_width=True,
        type="primary"
    ):
        st.success("Aquí se generará el PDF.")

with col2:

    if st.button(
        "❌ Cerrar Caja",
        use_container_width=True
    ):
        st.success("Caja cerrada correctamente.")
