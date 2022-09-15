from typing import Any

from slack_sdk import WebClient


class SlackWebClient:
    def __init__(self, token=None):
        self.client = WebClient(token=token)

    def enviar_mensaje_a_canal(self, canal: str, mensaje: dict[str, Any]):
        self.client.chat_postMessage(**mensaje, channel=canal)

    def enviar_mensaje_a_cada_usuario(self, mensaje: dict[str, Any]):
        members = self.client.users_list()["members"]
        for member in members:
            self.client.chat_postMessage(**mensaje, channel=member["id"])


class SlackMessage:
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self):
        self.username = "NoMasAccidentesBot"
        self.mensaje = []

    def generar_titulo(self, mensaje: str):
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": mensaje,
            },
        }
        self.mensaje.append(block)

    def generar_link(self, url: str, mensaje: str):
        block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (f":information_source: *<{url}|{mensaje}>*"),
            },
        }
        self.mensaje.append(block)

    def generar_mensaje_a_enviar(self):
        return {"username": self.username, "blocks": self.mensaje}
