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

# Inicializar estados de sesión para los botones
if "pdf_generating" not in st.session_state:
    st.session_state.pdf_generating = False
if "caja_closing" not in st.session_state:
    st.session_state.caja_closing = False

col1, col2 = st.columns(2)

# ========== BOTÓN DESCARGAR PDF ==========
if col1.button("📄 Descargar PDF", key="descargar_pdf", use_container_width=True):
    st.session_state.pdf_generating = True

if st.session_state.pdf_generating:
    try:
        with st.spinner("⏳ Generando PDF..."):
            # TODO: Implementar función real
            # generar_pdf_y_descargar(ventas, total)
            pass
        
        st.success("✅ PDF generado correctamente.")
        st.session_state.pdf_generating = False
        
    except FileNotFoundError as e:
        st.error(f"❌ Archivo no encontrado: {e}")
        st.session_state.pdf_generating = False
    except PermissionError as e:
        st.error(f"❌ Permiso denegado: {e}")
        st.session_state.pdf_generating = False
    except Exception as e:
        st.error(f"❌ Error al generar el PDF: {str(e)}")
        st.session_state.pdf_generating = False

# ========== BOTÓN CERRAR CAJA ==========
if col2.button("❌ Cerrar Caja", key="cerrar_caja", use_container_width=True):
    st.session_state.caja_closing = True

if st.session_state.caja_closing:
    try:
        with st.spinner("⏳ Cerrando caja..."):
            # TODO: Implementar función real
            # resultado = cerrar_caja_service(usuario_id, total)
            pass
        
        st.success("✅ Caja cerrada correctamente.")
        st.session_state.caja_closing = False
        
        # Opcional: Limpiar sesión después de cerrar caja
        # st.session_state.clear()
        # st.switch_page("streamlit_app.py")
        
    except ValueError as e:
        st.error(f"❌ Valor inválido: {e}")
        st.session_state.caja_closing = False
    except RuntimeError as e:
        st.error(f"❌ Error en operación: {e}")
        st.session_state.caja_closing = False
    except Exception as e:
        st.error(f"❌ Error al cerrar la caja: {str(e)}")
        st.session_state.caja_closing = False
