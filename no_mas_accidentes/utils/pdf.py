from django.templatetags.static import static
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, StyleSheet1, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.flowables import Image, PageBreakIfNotEmpty, Spacer
from reportlab.rl_config import canvas_basefontname as _baseFontName


class PdfConstants:
    class Alineamientos:
        IZQUIERDA = "LEFT"

    class EstilosTexto:
        class Titulos:
            DEFAULT = "Title"
            TITULO_1 = "Heading1"
            TITULO_2 = "Heading2"
            TITULO_3 = "Heading3"
            TITULO_4 = "Heading4"
            TITULO_5 = "Heading5"
            TITULO_6 = "Heading6"

        class Cuerpos:
            NORMAL = "Normal"
            CUERPO = "BodyText"
            ITALICO = "Italic"
            JUSTIFICADO = "Justificado"
            CENTRADO = "CuerpoCentrado"

        class Otros:
            LISTA_PUNTO = "Bullet"
            DEFINICION = "Definition"
            CODIGO = "Code"
            LISTA_NO_ORDENADA = "UnorderedList"
            LISTA_ORDER = "OrderedList"


class PdfBuilder:
    def _generar_estilos(self) -> StyleSheet1:
        estilos = getSampleStyleSheet()
        estilos.add(
            ParagraphStyle(
                name="Justificado",
                fontName=_baseFontName,
                alignment=TA_JUSTIFY,
                fontSize=10,
                leading=12,
            )
        )
        estilos.add(
            ParagraphStyle(
                name="CuerpoCentrado",
                fontName=_baseFontName,
                alignment=TA_CENTER,
                fontSize=10,
                leading=12,
            )
        )
        return estilos

    def _generar_documento_base(self, nombre_archivo: str):
        doc = SimpleDocTemplate(
            f"/tmp/{nombre_archivo}.pdf",
            title=nombre_archivo,
            author="no-mas-accidentes",
        )
        return doc

    def agregar_texto(self, contenido: str, estilo: str):
        texto = Paragraph(text=contenido, style=self.estilos[estilo])
        self.elementos.append(texto)

    def agregar_imagen(self, path: str, ancho: float, alto: float, alineamiento: str):
        imagen = Image(
            static(path),
            width=ancho * inch,
            height=alto * inch,
            kind="proportional",
            hAlign=alineamiento,
        )
        self.elementos.append(imagen)

    def agregar_linea_en_blanco(self):
        linea_en_blanco = Spacer(width=1 * inch, height=0.5 * inch)
        self.elementos.append(linea_en_blanco)

    def agregar_salto_de_pagina(self):
        self.elementos.append(PageBreakIfNotEmpty())

    def generar_pdf(self):
        def agregar_a_cada_pagina(canvas, doc):
            canvas.saveState()
            canvas.drawString(inch, 0.75 * inch, "2022 © Prevención Chile LTDA")
            canvas.restoreState()

        self.documento.build(
            self.elementos,
            onFirstPage=agregar_a_cada_pagina,
            onLaterPages=agregar_a_cada_pagina,
        )

    def __init__(self, nombre_archivo: str):
        self.estilos = self._generar_estilos()
        self.documento = self._generar_documento_base(nombre_archivo=nombre_archivo)
        self.elementos = []
