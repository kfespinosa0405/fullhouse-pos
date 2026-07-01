from services.ui_config import ocultar_menu_streamlit
import streamlit as st
from datetime import datetime

from io import BytesIO
from reportlab.pdfgen import canvas

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

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "CIERRE DE CAJA")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, datetime.now().strftime("%d/%m/%Y"))

    y -= 35

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Pedido")
    pdf.drawString(140, y, "Fecha")
    pdf.drawString(360, y, "Total")

    y -= 20
    pdf.setFont("Helvetica", 10)

    if ventas:
        for pedido_id, fecha, monto in ventas:
            pdf.drawString(50, y, f"#{pedido_id}")
            pdf.drawString(140, y, str(fecha))
            pdf.drawString(360, y, f"${monto:.2f}")
            y -= 18

            if y < 60:
                pdf.showPage()
                y = 800
                pdf.setFont("Helvetica", 10)

    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"TOTAL DEL DÍA: ${total:.2f}")

    pdf.save()
    buffer.seek(0)

    st.download_button(
        "📄 Descargar PDF",
        data=buffer,
        file_name=f"cierre_caja_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary"
    )

with col2:

    if st.button(
        "❌ Cerrar Caja",
        use_container_width=True
    ):
        st.success("Caja cerrada correctamente.")
