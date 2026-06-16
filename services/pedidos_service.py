from datetime import datetime

from services.db import conectar


# =========================
# PEDIDO ABIERTO
# =========================

def obtener_pedido_abierto(mesa_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM pedidos
        WHERE mesa_id=?
        AND estado='ABIERTO'
    """, (mesa_id,))

    pedido = cursor.fetchone()

    conn.close()

    return pedido


# =========================
# CREAR PEDIDO
# =========================

def crear_pedido(mesa_id):

    conn = conectar()
    cursor = conn.cursor()

    fecha = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO pedidos(
            mesa_id,
            fecha,
            estado,
            total
        )
        VALUES(
            ?,
            ?,
            'ABIERTO',
            0
        )
    """, (
        mesa_id,
        fecha
    ))

    conn.commit()

    pedido_id = cursor.lastrowid


    conn.close()

    return pedido_id


# =========================
# AGREGAR PRODUCTO
# =========================

def guardar_detalle(
    pedido_id,
    producto_id,
    cantidad,
    precio_unitario
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            cantidad
        FROM detalle_pedidos
        WHERE pedido_id=?
        AND producto_id=?
    """, (
        pedido_id,
        producto_id
    ))

    existe = cursor.fetchone()

    if existe:

        nueva_cantidad = (
            existe[1] + cantidad
        )

        subtotal = (
            nueva_cantidad *
            precio_unitario
        )

        cursor.execute("""
            UPDATE detalle_pedidos
            SET cantidad=?,
                subtotal=?
            WHERE id=?
        """, (
            nueva_cantidad,
            subtotal,
            existe[0]
        ))

    else:

        subtotal = (
            cantidad *
            precio_unitario
        )

        cursor.execute("""
            INSERT INTO detalle_pedidos(
                pedido_id,
                producto_id,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES(
                ?,?,?,?,?
            )
        """, (
            pedido_id,
            producto_id,
            cantidad,
            precio_unitario,
            subtotal
        ))

    conn.commit()
    conn.close()


# =========================
# ACTUALIZAR CANTIDAD
# =========================

def actualizar_cantidad(
    pedido_id,
    producto_id,
    cantidad,
    precio_unitario
):

    conn = conectar()
    cursor = conn.cursor()

    subtotal = (
        cantidad *
        precio_unitario
    )

    cursor.execute("""
        UPDATE detalle_pedidos
        SET cantidad=?,
            subtotal=?
        WHERE pedido_id=?
        AND producto_id=?
    """, (
        cantidad,
        subtotal,
        pedido_id,
        producto_id
    ))

    conn.commit()
    conn.close()


# =========================
# ELIMINAR PRODUCTO
# =========================

def eliminar_producto(
    pedido_id,
    producto_id
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM detalle_pedidos
        WHERE pedido_id=?
        AND producto_id=?
    """, (
        pedido_id,
        producto_id
    ))

    conn.commit()
    conn.close()


# =========================
# DETALLE
# =========================

def obtener_detalle(pedido_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.producto_id,
            p.nombre,
            d.cantidad,
            d.precio_unitario
        FROM detalle_pedidos d
        INNER JOIN productos p
            ON p.id = d.producto_id
        WHERE d.pedido_id=?
        ORDER BY p.nombre
    """, (pedido_id,))

    datos = cursor.fetchall()

    conn.close()

    return datos


# =========================
# TOTAL
# =========================

def actualizar_total(
    pedido_id,
    total
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pedidos
        SET total=?
        WHERE id=?
    """, (
        total,
        pedido_id
    ))

    conn.commit()
    conn.close()


def obtener_total_pedido(
    pedido_id
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT total
        FROM pedidos
        WHERE id=?
    """, (pedido_id,))

    dato = cursor.fetchone()

    conn.close()

    if dato:
        return dato[0]

    return 0


# =========================
# CERRAR PEDIDO
# =========================

def cerrar_pedido(
    pedido_id
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pedidos
        SET estado='CERRADO'
        WHERE id=?
    """, (pedido_id,))

    conn.commit()
    conn.close()