from pathlib import Path
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from services.pedidos_service import obtener_detalle


ANCHO_TICKET_MM = 58


def imprimir_ticket(
    pedido_id,
    total
):

    try:

        items = obtener_detalle(
            pedido_id
        )

        alto_mm = 90 + (len(items) * 12)

        carpeta = Path("tickets")

        carpeta.mkdir(
            exist_ok=True
        )

        archivo = carpeta / f"ticket_{pedido_id}.pdf"

        ancho = ANCHO_TICKET_MM * mm
        alto = alto_mm * mm

        pdf = canvas.Canvas(
            str(archivo),
            pagesize=(ancho, alto)
        )

        y = alto - 15

        pdf.setFont(
            "Helvetica-Bold",
            10
        )

        pdf.drawCentredString(
            ancho / 2,
            y,
            "FULL HOUSE"
        )

        y -= 15

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.drawCentredString(
            ancho / 2,
            y,
            "TICKET DE VENTA"
        )

        y -= 12

        fecha_hora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        pdf.setFont(
            "Helvetica",
            7
        )

        pdf.drawCentredString(
            ancho / 2,
            y,
            fecha_hora
        )

        y -= 15

        pdf.line(
            5,
            y,
            ancho - 5,
            y
        )

        y -= 12

        for item in items:

            nombre = str(item[1])

            cantidad = float(item[2])

            precio = float(item[3])

            subtotal = cantidad * precio

            pdf.setFont(
                "Helvetica-Bold",
                7
            )

            pdf.drawString(
                5,
                y,
                nombre[:28]
            )

            y -= 10

            pdf.setFont(
                "Helvetica",
                7
            )

            pdf.drawString(
                5,
                y,
                f"{int(cantidad)} x ${precio:.2f}"
            )

            pdf.drawRightString(
                ancho - 5,
                y,
                f"${subtotal:.2f}"
            )

            y -= 12

        pdf.line(
            5,
            y,
            ancho - 5,
            y
        )

        y -= 15

        pdf.setFont(
            "Helvetica-Bold",
            10
        )

        pdf.drawString(
            5,
            y,
            "TOTAL:"
        )

        pdf.drawRightString(
            ancho - 5,
            y,
            f"${total:.2f}"
        )

        y -= 20

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.drawCentredString(
            ancho / 2,
            y,
            "Gracias por su visita"
        )

        y -= 12

        pdf.drawCentredString(
            ancho / 2,
            y,
            "FULL HOUSE POS"
        )

        pdf.save()

        return archivo

    except Exception as e:

        print(
            "ERROR GENERANDO PDF:"
        )

        print(e)

        return None