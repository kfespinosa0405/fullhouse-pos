from services.ui_config import (
    ocultar_menu_streamlit
)

import streamlit as st
from pathlib import Path

from services.categorias_service import obtener_categorias
from services.productos_service import obtener_productos_por_categoria
from services.busqueda_service import buscar_productos

from services.mesas_service import (
    obtener_id_mesa,
    cambiar_estado
)

from services.pedidos_service import (
    obtener_pedido_abierto,
    crear_pedido,
    guardar_detalle,
    actualizar_cantidad,
    actualizar_total,
    obtener_detalle,
    eliminar_producto
)

from services.impresion_service import imprimir_ticket

if not st.session_state.get("logueado", False):
    st.switch_page("streamlit_app.py")

if "mesa_actual" not in st.session_state:
    st.warning("No se seleccionó ninguna mesa.")
    st.stop()

st.set_page_config(page_title="Pedido", layout="wide")
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

nombre_mesa = st.session_state["mesa_actual"]
mesa_id = obtener_id_mesa(nombre_mesa)

pedido = obtener_pedido_abierto(mesa_id)

if pedido:
    pedido_id = pedido[0]
else:
    pedido_id = crear_pedido(mesa_id)


def agregar_producto(producto):
    guardar_detalle(pedido_id, producto[0], 1, producto[2])
    st.rerun()


def cambiar_cantidad(producto_id, nueva_cantidad, precio):
    if nueva_cantidad <= 0:
        eliminar_producto(pedido_id, producto_id)
    else:
        actualizar_cantidad(
            pedido_id,
            producto_id,
            nueva_cantidad,
            precio
        )
    st.rerun()


def confirmar_pedido():
    cambiar_estado(nombre_mesa, "OCUPADA")
    st.success("Pedido confirmado correctamente")


st.title(f"Mesa {nombre_mesa}")
st.divider()

col1, col2, col3 = st.columns([1, 2, 2])

with col1:

    st.subheader("Categorías")

    texto_busqueda = st.text_input("Buscar producto")

    if st.button("Buscar", use_container_width=True):
        st.session_state["busqueda"] = buscar_productos(
            texto_busqueda
        )

    st.divider()

    categorias = obtener_categorias()

    for cat_id, nombre in categorias:

        if st.button(
            nombre,
            key=f"cat_{cat_id}",
            use_container_width=True
        ):
            st.session_state["productos"] = (
                obtener_productos_por_categoria(cat_id)
            )

with col2:

    st.subheader("Productos")

    productos = st.session_state.get(
        "productos",
        []
    )

    if "busqueda" in st.session_state:
        productos = st.session_state["busqueda"]

    for producto in productos:

        c1, c2 = st.columns([4, 1])

        with c1:
            st.write(
                f"{producto[1]} - ${producto[2]:.2f}"
            )

        with c2:

            if st.button(
                "Agregar",
                key=f"ag_{producto[0]}"
            ):
                agregar_producto(producto)

with col3:

    st.subheader("Pedido")

    items = obtener_detalle(pedido_id)

    total_actual = 0

    for pid, nombre, cantidad, precio in items:

        subtotal = cantidad * precio
        total_actual += subtotal

        c1, c2, c3, c4, c5, c6 = st.columns(
            [4, 1, 2, 1, 1, 1]
        )

        c1.write(nombre)
        c2.write(f"x{cantidad}")
        c3.write(f"${subtotal:.2f}")

        if c4.button("+", key=f"plus_{pid}"):
            cambiar_cantidad(
                pid,
                cantidad + 1,
                precio
            )

        if c5.button("-", key=f"minus_{pid}"):
            cambiar_cantidad(
                pid,
                cantidad - 1,
                precio
            )

        if c6.button("X", key=f"del_{pid}"):
            eliminar_producto(pedido_id, pid)
            st.rerun()

    actualizar_total(
        pedido_id,
        total_actual
    )

    st.divider()

    st.subheader(
        f"Total: ${total_actual:.2f}"
    )

    if st.button(
        "Confirmar Pedido",
        use_container_width=True
    ):
        confirmar_pedido()

    if st.button(
        "Generar Ticket",
        use_container_width=True
    ):

        archivo = imprimir_ticket(
            pedido_id,
            total_actual
        )

        if archivo:
            st.session_state["ticket_pdf"] = str(
                archivo
            )

    if st.session_state.get("ticket_pdf"):

        ruta = Path(
            st.session_state["ticket_pdf"]
        )

        if ruta.exists():

            with open(ruta, "rb") as pdf:

                st.download_button(
                    label="Descargar Ticket",
                    data=pdf,
                    file_name=ruta.name,
                    mime="application/pdf",
                    use_container_width=True
                )

    if st.button(
        "Cobrar",
        use_container_width=True
    ):

        st.session_state["pedido_id"] = pedido_id
        st.session_state["mesa_actual"] = nombre_mesa
        st.session_state["total_cobro"] = total_actual

        cambiar_estado(
            nombre_mesa,
            "CUENTA"
        )

        st.switch_page(
            "pages/cobro.py"
        )

    if st.button(
        "Volver al mapa",
        use_container_width=True
    ):

        st.switch_page(
            "pages/mapa_restaurante.py"
        )

