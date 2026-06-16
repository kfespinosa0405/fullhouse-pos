from services.db import conectar


def buscar_productos(texto):

    texto = texto.strip()

    conn = conectar()

    cursor = conn.cursor()

    if texto:

        cursor.execute("""
            SELECT
                id,
                nombre,
                precio
            FROM productos
            WHERE nombre LIKE ?
            ORDER BY nombre
        """, (f"%{texto}%",))

    else:

        cursor.execute("""
            SELECT
                id,
                nombre,
                precio
            FROM productos
            ORDER BY nombre
        """)

    datos = cursor.fetchall()

    conn.close()

    return datos