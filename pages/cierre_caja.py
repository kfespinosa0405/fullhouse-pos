from services.ui_config import ocultar_menu_streamlit
import streamlit as st
from datetime import datetime
import logging

from services.caja_service import (
    ventas_del_dia,
    total_del_dia
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Inicializar estados de sesión - SOLO UNA VEZ al inicio
if "pdf_loading" not in st.session_state:
    st.session_state.pdf_loading = False
if "caja_loading" not in st.session_state:
    st.session_state.caja_loading = False

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

# ========== CALLBACK DESCARGAR PDF ==========
def generar_pdf_callback():
    """Callback para generar PDF - se ejecuta UNA SOLA VEZ"""
    st.session_state.pdf_loading = True
    
    try:
        logger.info("Iniciando generación de PDF...")
        
        # TODO: Implementar función real
        # from services.pdf_service import generar_pdf_y_descargar
        # generar_pdf_y_descargar(ventas, total)
        
        # Simulación de éxito
        logger.info("PDF generado exitosamente")
        st.success("✅ PDF generado correctamente.")
        
    except FileNotFoundError as e:
        logger.error(f"Archivo no encontrado: {e}")
        st.error(f"❌ Archivo no encontrado: {e}")
    except PermissionError as e:
        logger.error(f"Permiso denegado: {e}")
        st.error(f"❌ Permiso denegado: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        st.error(f"❌ Error al generar el PDF: {str(e)}")
    finally:
        st.session_state.pdf_loading = False

# ========== CALLBACK CERRAR CAJA ==========
def cerrar_caja_callback():
    """Callback para cerrar caja - se ejecuta UNA SOLA VEZ"""
    st.session_state.caja_loading = True
    
    try:
        logger.info("Iniciando cierre de caja...")
        
        # TODO: Implementar función real
        # from services.caja_service import cerrar_caja_service
        # resultado = cerrar_caja_service(st.session_state.usuario_id, total)
        
        # Simulación de éxito
        logger.info("Caja cerrada exitosamente")
        st.success("✅ Caja cerrada correctamente.")
        
        # Opcional: Redireccionar después de cerrar
        # import time
        # time.sleep(2)
        # st.switch_page("streamlit_app.py")
        
    except ValueError as e:
        logger.error(f"Valor inválido: {e}")
        st.error(f"❌ Valor inválido: {e}")
    except RuntimeError as e:
        logger.error(f"Error en operación: {e}")
        st.error(f"❌ Error en operación: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        st.error(f"❌ Error al cerrar la caja: {str(e)}")
    finally:
        st.session_state.caja_loading = False

# ========== BOTONES CON CALLBACKS ==========
# Los callbacks se ejecutan ANTES de que el script continúe

col1.button(
    "📄 Descargar PDF",
    key="descargar_pdf",
    use_container_width=True,
    on_click=generar_pdf_callback,
    disabled=st.session_state.pdf_loading
)

col2.button(
    "❌ Cerrar Caja",
    key="cerrar_caja",
    use_container_width=True,
    on_click=cerrar_caja_callback,
    disabled=st.session_state.caja_loading
)
