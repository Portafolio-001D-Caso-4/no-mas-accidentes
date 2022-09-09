import datetime

from no_mas_accidentes.administracion.constants import InformacionEmpresaPrevencionChile
from no_mas_accidentes.clientes.models import Contrato
from no_mas_accidentes.utils import pdf as pdf_utils


def generar_pdf_contrato_base(contrato: Contrato) -> str:
    nombre_archivo = f"contrato-{contrato.empresa.rut}"
    ahora = datetime.datetime.now()
    dia = ahora.day
    mes = ahora.month
    anno = ahora.year
    tabla_precios_base = [
        ["SERVICIO", "CANTIDAD MÁXIMA", "$ POR EXTRA"],
        [
            "VISITAS",
            f"{contrato.max_visitas_mensuales} mensuales",
            f"{int(contrato.valor_visita_extra):,}".replace(",", "."),
        ],
        [
            "CAPACITACIONES",
            f"{contrato.max_capacitaciones_mensuales} mensuales",
            f"{int(contrato.valor_capacitacion_extra):,}".replace(",", "."),
        ],
        [
            "ASESORIAS",
            f"{contrato.max_asesorias_mensuales} mensuales",
            f"{int(contrato.valor_asesoria_extra):,}".replace(",", "."),
        ],
        [
            "LLAMADAS",
            "Sin límite*",
            f"{int(contrato.valor_llamada_fuera_horario):,}".replace(",", "."),
        ],
        [
            "ACTUALIZACIONES DE REPORTE",
            f"{contrato.max_actualizaciones_mensuales_reporte_cliente} mensual",
            f"{int(contrato.valor_modificacion_reporte_extra):,}".replace(",", "."),
        ],
        [
            "ACTUALIZACIONES DE CHECKLIST",
            f"{contrato.max_actualizaciones_checklist_anuales} anual",
            f"{int(contrato.valor_modificacion_checklist_extra):,}".replace(",", "."),
        ],
    ]

    pdf = pdf_utils.PdfBuilder(nombre_archivo=nombre_archivo)

    pdf.agregar_texto(
        "CONTRATO DE PRESTACIÓN DE SERVICIOS",
        estilo=pdf_utils.PdfConstants.EstilosTexto.Titulos.DEFAULT,
    )
    pdf.agregar_texto(
        f"""
        En {InformacionEmpresaPrevencionChile.direccion} a {dia} de {mes} de {anno}, entre
        {InformacionEmpresaPrevencionChile.nombre} (razón social), RUT {InformacionEmpresaPrevencionChile.rut}
        que en adelante se denominará "<i>el mandatario</i>", y {contrato.empresa.nombre}(razón social),
        RUT {contrato.empresa.rut}, que en adelante se denominará "<i>el mandante</i>", han acordado el
        contrato de prestación de servicios que constan de la cláusulas que a continuación se exponen:
        """,
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    pdf.agregar_linea_en_blanco()
    pdf.agregar_texto(
        f"""
        <b>PRIMERO</b>: En virtud del presente contrato, el mandatorio se compromete a ejecutar el siguiente encargo:
        {InformacionEmpresaPrevencionChile.servicio}
        """,
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    pdf.agregar_linea_en_blanco()
    pdf.agregar_texto(
        """
        <b>SEGUNDO</b>: Por el servicio que realizará el mandatario, el mandante pagará un
        valor base correspondiente a la suma de $
        """
        + f"{int(contrato.valor_base):,}".replace(",", "."),
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    pdf.agregar_linea_en_blanco()
    pdf.agregar_texto(
        """
        <b>TERCERO</b>: El mandatario se obliga a realizar los siguientes servicios,
        incluyendo servicios extra con un valor adicional:
        """,
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    pdf.agregar_linea_en_blanco()
    pdf.agregar_tabla(datos_matriz=tabla_precios_base)
    pdf.agregar_linea_en_blanco()
    pdf.agregar_texto(
        f"""
        <b>CUARTO</b>: El horario de llamadas permitido es de Lunes a Viernes, desde las
        {contrato.inicio_horario_llamadas:%H:%M} a {contrato.fin_horario_llamadas:%H:%M} hrs.
        Cualquier llamada extra será cargada según los valores descritos
        en el artículo TERCERO.
        """,
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    pdf.agregar_linea_en_blanco()
    pdf.agregar_texto(
        f"""
        <b>QUINTO</b>: La fecha de facturación tendrá lugar los {contrato.dia_facturacion} de cada mes.
        """,
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.JUSTIFICADO,
    )
    for _ in range(4):
        pdf.agregar_linea_en_blanco()

    pdf.agregar_texto(
        f"{'_' * 24} {'&nbsp;' * 12} {'_' * 24}",
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.CENTRADO,
    )
    pdf.agregar_texto(
        f"FIRMA EMPRESA {'&nbsp;' * 34} FIRMA CLIENTE",
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.CENTRADO,
    )
    pdf.agregar_texto(
        f"RUT {'&nbsp;' * 50} RUT",
        estilo=pdf_utils.PdfConstants.EstilosTexto.Cuerpos.CENTRADO,
    )
    pdf.generar_pdf()
    return nombre_archivo
