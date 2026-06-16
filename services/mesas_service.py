from services.db import conectar

conn = conectar()

cursor = conn.cursor()

cursor.execute("""
    UPDATE mesas
    SET estado='LIBRE'
""")

conn.commit()
conn.close()

from services.db import conectar


def obtener_mesas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            estado
        FROM mesas
        ORDER BY id
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


def obtener_estado(nombre_mesa):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT estado
        FROM mesas
        WHERE nombre=?
    """, (nombre_mesa,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return "LIBRE"


def cambiar_estado(
    nombre_mesa,
    nuevo_estado
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE mesas
        SET estado=?
        WHERE nombre=?
    """, (
        nuevo_estado,
        nombre_mesa
    ))

    conn.commit()

    conn.close()


def obtener_id_mesa(nombre):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM mesas
        WHERE nombre=?
    """, (nombre,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return None


def obtener_nombre_mesa(mesa_id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre
        FROM mesas
        WHERE id=?
    """, (mesa_id,))

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return resultado[0]

    return None