from services.db import conectar


def obtener_categorias():

    conn = None

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                nombre
            FROM categorias
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:

        print(
            "Error obteniendo categorías:",
            e
        )

        return []

    finally:

        if conn:
            conn.close()