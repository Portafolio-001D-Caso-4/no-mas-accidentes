import arrow
from django.contrib import messages
from django.db.models import Count
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from no_mas_accidentes.clientes.models import Empresa
from no_mas_accidentes.profesionales.business_logic.accidentabilidad import (
    calcular_accidentabilidad_por_profesional,
)
from no_mas_accidentes.profesionales.constants import app_name
from no_mas_accidentes.profesionales.forms import (
    ActualizarAsesoriaEmergenciaForm,
    ActualizarAsistenciaParticipanteCapacitacionForm,
    ActualizarAsistenciaParticipantesFormSetHelper,
    ActualizarCapacitacionForm,
    ActualizarChecklistForm,
    ActualizarOportunidadDeMejoraVisitaForm,
    ActualizarOportunidadDeMejoraVisitaFormSetHelper,
    ActualizarVisitaForm,
    DetalleEmpresaForm,
)
from no_mas_accidentes.profesionales.mixins import EsProfesionalMixin
from no_mas_accidentes.servicios.business_logic import (
    servicios as business_logic_servicios,
)
from no_mas_accidentes.servicios.constants import TIPOS_DE_SERVICIOS, TiposDeServicio
from no_mas_accidentes.servicios.forms import CrearOActualizarChecklistBaseForm
from no_mas_accidentes.servicios.models import (
    Checklist,
    ChecklistBase,
    OportunidadDeMejora,
    Participante,
    Servicio,
)


class Home(EsProfesionalMixin, TemplateView):
    template_name = f"{app_name}/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mes_actual = arrow.utcnow().datetime.month
        num_servicios_por_tipo = list(
            Servicio.objects.filter(
                profesional__usuario=self.request.user, realizado_en__month=mes_actual
            )
            .values("tipo")
            .order_by("tipo")
            .annotate(num_servicios=Count("tipo"))
        )
        context["num_visitas"] = sum(
            servicio["num_servicios"]
            for servicio in num_servicios_por_tipo
            if servicio["tipo"] == TiposDeServicio.VISITA
        )
        context["num_capacitaciones"] = sum(
            servicio["num_servicios"]
            for servicio in num_servicios_por_tipo
            if servicio["tipo"] == TiposDeServicio.CAPACITACION
        )
        context["num_asesorias"] = sum(
            servicio["num_servicios"]
            for servicio in num_servicios_por_tipo
            if servicio["tipo"]
            in (
                TiposDeServicio.ASESORIA_EMERGENCIA,
                TiposDeServicio.ASESORIA_FISCALIZACION,
            )
        )
        context["num_llamadas"] = sum(
            servicio["num_servicios"]
            for servicio in num_servicios_por_tipo
            if servicio["tipo"] == TiposDeServicio.LLAMADA
        )
        context["num_accidentes"] = sum(
            servicio["num_servicios"]
            for servicio in num_servicios_por_tipo
            if servicio["tipo"] == TiposDeServicio.ASESORIA_EMERGENCIA
        )
        context[
            "porcentaje_accidentabilidad"
        ] = calcular_accidentabilidad_por_profesional(
            profesional_id=self.request.user.pk
        )
        context[
            "agendas"
        ] = business_logic_servicios.traer_context_data_de_servicios_por_profesional(
            id_profesional=self.request.user.pk
        )
        context["num_empresas_asignadas"] = Empresa.objects.filter(
            profesional_asignado_id=self.request.user.pk
        ).count()
        context["servicio_en_progreso"] = Servicio.objects.filter(
            profesional=self.request.user.pk,
            agendado_para__lte=arrow.utcnow().datetime,
            realizado_en__isnull=True,
        ).first()
        return context


class ListaEmpresasAsignadasView(EsProfesionalMixin, ListView):
    queryset = Empresa.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:empresas_asignadas_lista")
    ordering = "id"
    paginate_by = 10
    template_name = f"{app_name}/lista_empresas_asignadas.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        queryset = self.queryset.order_by(self.ordering)
        # solo puede ver sus empresas asignadas
        queryset = queryset.filter(profesional_asignado_id=self.request.user.pk)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        return context


class DetalleEmpresaInformacionView(EsProfesionalMixin, DetailView):
    template_name = f"{app_name}/detalle_empresa/informacion.html"
    queryset = Empresa.objects.all()

    def get_queryset(self):
        return self.queryset.filter(profesional_asignado_id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        context["form"] = DetalleEmpresaForm(instance=self.object)
        return context


home_view = Home.as_view()
lista_empresas_asignadas_view = ListaEmpresasAsignadasView.as_view()
detalle_empresa_informacion_view = DetalleEmpresaInformacionView.as_view()


class ListaServiciosAsignadosView(EsProfesionalMixin, ListView):
    queryset = Servicio.objects.all()
    fields = "__all__"
    success_url = reverse_lazy(f"{app_name}:servicios_asignados_lista")
    ordering = "-agendado_para"
    paginate_by = 10
    template_name = f"{app_name}/lista_servicios_asignados.html"

    def get_queryset(self):
        filtro_rut = self.request.GET.get("filtro_rut")
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada"
        )
        filtro_tipo_seleccionado = self.request.GET.get("filtro_tipo_seleccionado")
        filtro_es_realizado = self.request.GET.get("filtro_es_realizado")
        queryset = self.queryset.order_by(self.ordering)
        # solo puede ver sus servicios asignadas
        queryset = queryset.filter(profesional_id=self.request.user.pk)
        if filtro_rut:
            rut_a_buscar = str(filtro_rut).upper()
            queryset = queryset.filter(rut=rut_a_buscar)
        if filtro_empresa_seleccionada:
            queryset = queryset.filter(empresa_id=int(filtro_empresa_seleccionada))
        if filtro_tipo_seleccionado:
            queryset = queryset.filter(tipo=filtro_tipo_seleccionado)
        if filtro_es_realizado == "PENDIENTE":
            queryset = queryset.filter(realizado_en__isnull=True)
        elif filtro_es_realizado == "REALIZADA":
            queryset = queryset.filter(realizado_en__isnull=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_rut"] = self.request.GET.get("filtro_rut", "")
        context["filtro_tipo_seleccionado"] = self.request.GET.get(
            "filtro_tipo_seleccionado", ""
        )
        context["filtro_es_realizado"] = self.request.GET.get("filtro_es_realizado", "")
        # solo puede ver sus empresas asignadas
        context["filtro_tipos"] = TIPOS_DE_SERVICIOS
        context["filtro_empresas"] = Empresa.objects.filter(
            profesional_asignado_id=self.request.user.pk
        )
        filtro_empresa_seleccionada = self.request.GET.get(
            "filtro_empresa_seleccionada", ""
        )
        context["filtro_empresa_seleccionada"] = (
            int(filtro_empresa_seleccionada) if filtro_empresa_seleccionada else ""
        )
        return context


lista_servicios_asignados_view = ListaServiciosAsignadosView.as_view()


def crear_o_actualizar_checklist_base_view(request, pk: int):
    try:
        checklist: ChecklistBase = ChecklistBase.objects.get(empresa_id=pk)
        item_por_id = {
            f"item_{index}": item for index, item in enumerate(checklist.items, start=1)
        }
        data_inicial = {"numero_de_items": len(checklist.items), **item_por_id}
    except ChecklistBase.DoesNotExist:
        checklist = None
        data_inicial = {}

    if request.method == "POST":
        if data_inicial:
            # update
            form = CrearOActualizarChecklistBaseForm(
                request.POST,
                request=request,
                numero_de_items=request.POST.get("numero_de_items"),
                id_empresa=pk,
                initial=data_inicial,
            )
        else:
            # crear
            form = CrearOActualizarChecklistBaseForm(
                request.POST,
                request=request,
                numero_de_items=request.POST.get("numero_de_items"),
                id_empresa=pk,
            )
        if form.is_valid():
            form.save()
    else:
        form = CrearOActualizarChecklistBaseForm(
            request=request, id_empresa=pk, initial=data_inicial
        )
    return render(
        request,
        f"{app_name}/detalle_empresa/checklist/crear_checklist.html",
        {"form": form, "empresa": Empresa.objects.get(pk=pk)},
    )


class ActualizarAsesoriaEmergenciaView(EsProfesionalMixin, UpdateView):
    template_name = f"{app_name}/asesoria_emergencia/actualizar.html"
    form_class = ActualizarAsesoriaEmergenciaForm
    queryset = Servicio.objects.filter(tipo=TiposDeServicio.ASESORIA_EMERGENCIA)

    def get_success_message(self):
        return f"Asesoría de emergencia {self.object.id} actualizada satisfactoriamente"

    def form_valid(self, form):
        form.save()
        if form.terminado:
            messages.success(
                self.request,
                f"Asesoría de emergencia {self.object.id} finalizada satisfactoriamente",
            )
            return HttpResponseRedirect(reverse_lazy(f"{app_name}:home"))
        messages.success(self.request, self.get_success_message())
        return HttpResponseRedirect(
            reverse_lazy(
                f"{app_name}:asesoria_emergencia_actualizar",
                kwargs={"pk": self.object.pk},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        context["accidente"] = self.object.evento_set.first()
        return context


actualizar_asesoria_emergencia_view = ActualizarAsesoriaEmergenciaView.as_view()


class ActualizarCapacitacionView(EsProfesionalMixin, UpdateView):
    template_name = f"{app_name}/capacitacion/actualizar.html"
    form_class = ActualizarCapacitacionForm
    queryset = Servicio.objects.filter(tipo=TiposDeServicio.CAPACITACION)

    def get_success_message(self):
        return f"Capacitación {self.object.id} actualizada satisfactoriamente"

    def form_valid(self, form):
        form.save()
        if form.terminado:
            messages.success(
                self.request,
                f"Capacitación {self.object.id} finalizada satisfactoriamente",
            )
            return HttpResponseRedirect(reverse_lazy(f"{app_name}:home"))
        messages.success(self.request, self.get_success_message())
        return HttpResponseRedirect(
            reverse_lazy(
                f"{app_name}:capacitacion_actualizar",
                kwargs={"pk": self.object.pk},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object
        return context


def modificar_asistencia_capacitacion_view(request, pk: int):
    capacitacion: Servicio = Servicio.objects.filter(
        tipo=TiposDeServicio.CAPACITACION
    ).get(pk=pk)
    participantes = capacitacion.participante_set.all().order_by("rut")
    helper = ActualizarAsistenciaParticipantesFormSetHelper()
    actualizar_participantes_forms = modelformset_factory(
        Participante,
        form=ActualizarAsistenciaParticipanteCapacitacionForm,
        min_num=capacitacion.num_participantes,
        validate_min=True,
        extra=0,
    )

    if request.method == "POST":
        formset = actualizar_participantes_forms(
            data=request.POST, queryset=participantes
        )
        if formset.is_valid():
            formset.save()
            messages.success(
                request=request, message="Asistencia modificada satisfactoriamente"
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    f"{app_name}:capacitacion_actualizar_asistencia", kwargs={"pk": pk}
                )
            )
    else:
        formset = actualizar_participantes_forms(queryset=participantes)

    return render(
        request,
        f"{app_name}/capacitacion/actualizar_asistencia.html",
        {
            "formset": formset,
            "empresa": Empresa.objects.get(pk=capacitacion.empresa_id),
            "helper": helper,
            "object": capacitacion,
        },
    )


actualizar_capacitacion_view = ActualizarCapacitacionView.as_view()
actualizar_asistencia_capacitacion_view = modificar_asistencia_capacitacion_view


class ActualizarVisitaView(EsProfesionalMixin, UpdateView):
    template_name = f"{app_name}/visita/actualizar.html"
    form_class = ActualizarVisitaForm
    queryset = Servicio.objects.filter(tipo=TiposDeServicio.VISITA)

    def get_success_message(self):
        return f"Visita {self.object.id} actualizada satisfactoriamente"

    def form_valid(self, form):
        form.save()
        if form.terminado:
            messages.success(
                self.request,
                f"Visita {self.object.id} finalizada satisfactoriamente",
            )
            return HttpResponseRedirect(reverse_lazy(f"{app_name}:home"))
        messages.success(self.request, self.get_success_message())
        return HttpResponseRedirect(
            reverse_lazy(
                f"{app_name}:visita_actualizar",
                kwargs={"pk": self.object.pk},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["empresa"] = self.object.empresa
        return context


def actualizar_checklist_view(request, pk: int):
    visita: Servicio = Servicio.objects.filter(tipo=TiposDeServicio.VISITA).get(pk=pk)

    checklist: Checklist = Checklist.objects.get(servicio=visita)
    item_por_id = {
        f"item_{index}": item for index, item in enumerate(checklist.items, start=1)
    }
    data_inicial = {"numero_de_items": len(checklist.items), **item_por_id}

    if request.method == "POST":
        form = ActualizarChecklistForm(
            request.POST,
            request=request,
            numero_de_items=request.POST.get("numero_de_items"),
            id_servicio=pk,
            initial=data_inicial,
        )

        if form.is_valid():
            form.save()
    else:
        form = ActualizarChecklistForm(
            request=request, id_servicio=pk, initial=data_inicial
        )
        # ver esta template
    return render(
        request,
        f"{app_name}/visita/actualizar_checklist.html",
        {"form": form, "empresa": visita.empresa, "object": visita},
    )


def actualizar_actividad_de_mejora_view(request, pk: int):
    visita: Servicio = Servicio.objects.filter(tipo=TiposDeServicio.VISITA).get(pk=pk)
    oportunidades_de_mejora = visita.oportunidaddemejora_set.all().order_by("contenido")
    helper = ActualizarOportunidadDeMejoraVisitaFormSetHelper()
    actualizar_oportunidades_de_mejora_forms = modelformset_factory(
        OportunidadDeMejora,
        form=ActualizarOportunidadDeMejoraVisitaForm,
        min_num=2,
        validate_min=True,
        extra=1,
        max_num=15,
        absolute_max=15,
    )

    if request.method == "POST":
        formset = actualizar_oportunidades_de_mejora_forms(
            data=request.POST, queryset=oportunidades_de_mejora
        )
        if formset.is_valid():
            instances = formset.save(commit=False)
            for oportunidad in instances:
                oportunidad.servicio = visita
                oportunidad.save()
            formset.save_m2m()
            messages.success(
                request=request, message="Actividades modificadas satisfactoriamente"
            )
            return HttpResponseRedirect(
                reverse_lazy(
                    f"{app_name}:visita_actualizar_actividad_mejora", kwargs={"pk": pk}
                )
            )
    else:
        formset = actualizar_oportunidades_de_mejora_forms(
            queryset=oportunidades_de_mejora
        )

    return render(
        request,
        f"{app_name}/visita/actividades_de_mejora.html",
        {
            "formset": formset,
            "empresa": Empresa.objects.get(pk=visita.empresa_id),
            "helper": helper,
            "object": visita,
        },
    )


actualizar_visita_view = ActualizarVisitaView.as_view()
actualizar_actividad_de_mejora_view = actualizar_actividad_de_mejora_view
actualizar_checklist_view = actualizar_checklist_view
