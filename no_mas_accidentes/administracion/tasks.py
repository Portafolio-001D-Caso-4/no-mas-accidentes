from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

from config import celery_app
from no_mas_accidentes.clientes.models import FacturaMensual


@celery_app.task()
def enviar_recordatorio_no_pago(id_factura_mensual: int, url_de_pago: str):
    factura_mensual = FacturaMensual.objects.get(id=id_factura_mensual)
    current_site = Site.objects.get_current()
    send_mail(
        "Recordatorio de pago",
        render_to_string(
            "account/email/recordatorio_no_pago.txt",
            context={
                "current_site": current_site,
                "factura_mensual": factura_mensual,
                "empresa": factura_mensual.contrato.empresa,
                "url_de_pago": url_de_pago,
            },
        ),
        "no-mas-accientes@example.com",
        list(factura_mensual.contrato.empresa.user_set.values_list("email", flat=True)),
        fail_silently=False,
    )
