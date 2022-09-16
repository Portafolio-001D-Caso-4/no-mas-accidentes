import pytest
from django.contrib.auth.models import Group

from no_mas_accidentes.profesionales.models import Profesional
from no_mas_accidentes.users.models import User
from no_mas_accidentes.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def usuario_cliente(db) -> User:
    usuario = UserFactory()
    grupo = Group.objects.get(name="cliente")
    usuario.groups.add(grupo)
    return usuario


@pytest.fixture
def usuario_profesional(db) -> User:
    usuario = UserFactory()
    grupo = Group.objects.get(name="profesional")
    usuario.groups.add(grupo)
    Profesional(usuario=usuario).save()
    return usuario
