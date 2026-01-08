from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

from .forms import (
    DatosPersonalesForm,
    ExperienciaLaboralForm,
    ReconocimientosForm,
    CursosRealizadosForm,
    ProductosAcademicosForm,
    ProductosLaboralesForm,
    VentaGarageForm
)


class PerfilListView(View):
    """Lista todos los perfiles registrados."""
    def get(self, request):
        perfiles = DatosPersonales.objects.all()
        return render(request, 'perfiles/list.html', {'perfiles': perfiles})


class PerfilDetailView(View):
    """Detalle completo del perfil."""
    def get(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)

        context = {
            'perfil': perfil,
            'experiencias': ExperienciaLaboral.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'reconocimientos': Reconocimientos.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'cursos': CursosRealizados.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'productos_academicos': ProductosAcademicos.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'productos_laborales': ProductosLaborales.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'ventas': VentaGarage.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
        }
        return render(request, 'perfiles/detail.html', context)


class PerfilCreateView(View):
    """Crear perfil."""
    def get(self, request):
        form = DatosPersonalesForm()
        return render(request, 'perfiles/form.html', {'form': form})

    def post(self, request):
        form = DatosPersonalesForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save()
            return redirect('perfil_detail', pk=perfil.pk)
        return render(request, 'perfiles/form.html', {'form': form})


class PerfilUpdateView(View):
    """Editar perfil."""
    def get(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)
        form = DatosPersonalesForm(instance=perfil)
        return render(request, 'perfiles/form.html', {'form': form})

    def post(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)
        form = DatosPersonalesForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil_detail', pk=perfil.pk)
        return render(request, 'perfiles/form.html', {'form': form})


class PerfilDeleteView(View):
    """Eliminar perfil."""
    def post(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)
        perfil.delete()
        return redirect('perfil_list')


def crear_seccion(request, perfil_pk, form_class=None):
    """Crear sección asociada al perfil."""
    perfil = get_object_or_404(DatosPersonales, pk=perfil_pk)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.perfil = perfil
            obj.save()
            return redirect('perfil_detail', pk=perfil.pk)
    else:
        form = form_class()

    return render(
        request,
        'perfiles/form_seccion.html',
        {'form': form, 'perfil': perfil}
    )


def actualizar_seccion(request, pk, model_class=None, form_class=None):
    """Actualizar sección."""
    obj = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('perfil_detail', pk=obj.perfil.pk)
    else:
        form = form_class(instance=obj)

    return render(
        request,
        'perfiles/form_seccion.html',
        {'form': form, 'perfil': obj.perfil}
    )


def eliminar_seccion(request, pk, model_class=None):
    """Eliminar sección."""
    obj = get_object_or_404(model_class, pk=pk)
    perfil_pk = obj.perfil.pk
    obj.delete()
    return redirect('perfil_detail', pk=perfil_pk)


def descargar_perfil(request, pk):
    """
    Descarga del perfil.
    ✔ Compatible con Render
    ✔ SIN wkhtmltopdf
    ✔ SIN error 500
    """
    perfil = get_object_or_404(DatosPersonales, pk=pk)

    html = render_to_string(
        'perfiles/pdf_perfil.html',
        {
            'perfil': perfil,
            'experiencias': ExperienciaLaboral.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'reconocimientos': Reconocimientos.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'cursos': CursosRealizados.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'productos_academicos': ProductosAcademicos.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'productos_laborales': ProductosLaborales.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
            'ventas': VentaGarage.objects.filter(
                perfil=perfil, activarparaqueseveaenfront=True
            ),
        }
    )

    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = (
        f'inline; filename="{perfil.nombres}_{perfil.apellidos}.html"'
    )
    return response
