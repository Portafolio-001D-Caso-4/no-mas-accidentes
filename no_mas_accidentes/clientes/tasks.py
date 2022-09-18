from django.conf import settings

from config import celery_app
from no_mas_accidentes.utils.slack import SlackMessage, SlackWebClient


@celery_app.task()
def enviar_alerta():
    cliente = SlackWebClient(token=settings.SLACK_TOKEN)
    mensaje = SlackMessage()
    titulo = "Se ha generado un nuevo accidente, por favor revisar inmediatamente"
    mensaje.generar_titulo(mensaje=titulo)
    mensaje.generar_link(url="google.com", mensaje="Ver alerta en sitio web")
    contenido_a_enviar = mensaje.generar_mensaje_a_enviar()
    cliente.enviar_mensaje_a_canal(
        canal="alertas", texto=titulo, mensaje=contenido_a_enviar
    )
    cliente.enviar_mensaje_a_cada_usuario(texto=titulo, mensaje=contenido_a_enviar)


@celery_app.task()
def enviar_alerta_pago_realizado(usuario_id: int, empresa_id: int, factura_id: int):
    cliente = SlackWebClient(token=settings.SLACK_TOKEN)
    mensaje = SlackMessage()
    titulo = (
        f"Se ha generado un nuevo pago por usuario {usuario_id} a empresa {empresa_id} "
        f"(factura mensual {factura_id})"
    )
    mensaje.generar_titulo(mensaje=titulo)
    mensaje.generar_link(url="google.com", mensaje="Ver pago en sitio web")
    contenido_a_enviar = mensaje.generar_mensaje_a_enviar()
    cliente.enviar_mensaje_a_canal(
        canal="pagos", texto=titulo, mensaje=contenido_a_enviar
    )
    cliente.enviar_mensaje_a_cada_usuario(texto=titulo, mensaje=contenido_a_enviar)
