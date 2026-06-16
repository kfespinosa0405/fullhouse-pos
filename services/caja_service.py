from services.db import conectar


def ventas_del_dia():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            fecha,
            total
        FROM pedidos
        WHERE estado='CERRADO'
        AND DATE(fecha)=DATE('now','localtime')
        ORDER BY fecha
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


def total_del_dia():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(total),0)
        FROM pedidos
        WHERE estado='CERRADO'
        AND DATE(fecha)=DATE('now','localtime')
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total