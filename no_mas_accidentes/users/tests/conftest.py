import pytest
from django.contrib.auth.models import Group

from no_mas_accidentes.users.models import User
from no_mas_accidentes.users.tests.factories import UserFactory


@pytest.fixture
def usuario_cliente(db) -> User:
    usuario = UserFactory()
    grupo = Group.objects.get(name="cliente")
    usuario.groups.add(grupo)
    return usuario
