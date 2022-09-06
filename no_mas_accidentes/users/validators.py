import string
from itertools import cycle

from django.core.exceptions import ValidationError


def validar_rut(rut: str) -> None:
    rut = rut.upper()
    caracteres_permitidos = set(string.digits + "K")
    if not set(rut) <= caracteres_permitidos:
        raise ValidationError("Solo se permiten números y K")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if not (str(res) == dv or (dv == "K" and res == 10)):
        raise ValidationError("Rut es inválido")
