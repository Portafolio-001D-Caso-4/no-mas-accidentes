import pytest
from django.core.exceptions import ValidationError

from no_mas_accidentes.users import validators


class TestValidarRut:
    @pytest.mark.parametrize(
        "rut",
        ("192140730", "13338250k", "13338250K", "136530682", "250474474", "204186642"),
    )
    def test_rut_valido_no_lanza_exception(self, rut):
        validators.validar_rut(rut=rut)

    @pytest.mark.parametrize(
        "rut",
        (
            "19214073L",
            "13338250.k",
            "13338250-K",
            "13653068-2",
            "13653068-12",
        ),
    )
    def test_rut_invalido(self, rut):
        with pytest.raises(ValidationError):
            validators.validar_rut(rut=rut)
