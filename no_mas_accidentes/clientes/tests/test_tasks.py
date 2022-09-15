import pytest

from no_mas_accidentes.clientes.tasks import enviar_alerta


@pytest.mark.skip("Envia mensaje a la API de Slack")
def test_enviar_alerta():
    enviar_alerta()
