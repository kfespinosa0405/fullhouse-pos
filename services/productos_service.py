from services.db import conectar


def obtener_productos_por_categoria(categoria_id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            precio
        FROM productos
        WHERE categoria_id=?
        ORDER BY nombre
    """, (categoria_id,))

    productos = cursor.fetchall()

    conn.close()

    return productos


def obtener_producto(producto_id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            precio
        FROM productos
        WHERE id=?
    """, (producto_id,))

    producto = cursor.fetchone()

    conn.close()

    return producto


def obtener_todos_los_productos():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            precio
        FROM productos
        ORDER BY nombre
    """)

    productos = cursor.fetchall()

    conn.close()

    return productos