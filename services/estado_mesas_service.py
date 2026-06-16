from services.db import conectar


def ocupar_mesa(nombre_mesa):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE mesas
        SET estado='OCUPADA'
        WHERE nombre=?
    """, (nombre_mesa,))

    conn.commit()

    conn.close()


def liberar_mesa(nombre_mesa):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE mesas
        SET estado='LIBRE'
        WHERE nombre=?
    """, (nombre_mesa,))

    conn.commit()

    conn.close()