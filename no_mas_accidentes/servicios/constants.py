class TiposDeServicio:
    ASESORIA_EMERGENCIA = "ASESORIA EMERGENCIA"
    ASESORIA_FISCALIZACION = "ASESORIA FISCALIZACION"
    CAPACITACION = "CAPACITACION"
    VISITA = "VISITA"
    LLAMADA = "LLAMADA"


duracion_en_hrs_por_servicio = {
    TiposDeServicio.ASESORIA_EMERGENCIA: 3,
    TiposDeServicio.ASESORIA_FISCALIZACION: 3,
    TiposDeServicio.CAPACITACION: 2,
    TiposDeServicio.VISITA: 2,
}


OPCIONES_DE_SERVICIOS = [
    (
        TiposDeServicio.ASESORIA_EMERGENCIA,
        TiposDeServicio.ASESORIA_EMERGENCIA,
    ),
    (
        TiposDeServicio.ASESORIA_FISCALIZACION,
        TiposDeServicio.ASESORIA_FISCALIZACION,
    ),
    (
        TiposDeServicio.CAPACITACION,
        TiposDeServicio.CAPACITACION,
    ),
    (
        TiposDeServicio.VISITA,
        TiposDeServicio.VISITA,
    ),
    (
        TiposDeServicio.LLAMADA,
        TiposDeServicio.LLAMADA,
    ),
]
