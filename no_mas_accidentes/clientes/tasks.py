from django.conf import settings

from config import celery_app
from no_mas_accidentes.utils.slack import SlackMessage, SlackWebClient


@celery_app.task()
def enviar_alerta():
    cliente = SlackWebClient(token=settings.SLACK_TOKEN)
    mensaje = SlackMessage()
    mensaje.generar_titulo(
        mensaje="Se ha generado un nuevo accidente, por favor revisar inmediatamente"
    )
    mensaje.generar_link(url="google.com", mensaje="Ver alerta en sitio web")
    contenido_a_enviar = mensaje.generar_mensaje_a_enviar()
    cliente.enviar_mensaje_a_canal(canal="alertas", mensaje=contenido_a_enviar)
    cliente.enviar_mensaje_a_cada_usuario(mensaje=contenido_a_enviar)
