from django.shortcuts import render, get_object_or_404, redirect 
from django.views import View 
from django.http import HttpResponse 
from django.template.loader import render_to_string  
import pdfkit  

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
    """
    Lista todos los perfiles registrados.
    """
    def get(self, request):
        perfiles = DatosPersonales.objects.all()  # Obtenemos todos los perfiles
        return render(request, 'perfiles/list.html', {'perfiles': perfiles})  # Renderizamos template con lista


class PerfilDetailView(View):
    """
    Muestra el detalle de un perfil específico.
    También incluye todas las secciones asociadas (experiencia, cursos, ventas, etc.).
    """
    def get(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)  
        context = {
            'perfil': perfil,
            'experiencias': ExperienciaLaboral.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'reconocimientos': Reconocimientos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'cursos': CursosRealizados.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'productos_academicos': ProductosAcademicos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'productos_laborales': ProductosLaborales.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'ventas': VentaGarage.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
        }
        return render(request, 'perfiles/detail.html', context) 


class PerfilCreateView(View):
    """
    Crear un nuevo perfil de usuario.
    """
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
    """
    Editar un perfil existente.
    """
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
    """
    Eliminar un perfil.
    """
    def post(self, request, pk):
        perfil = get_object_or_404(DatosPersonales, pk=pk)
        perfil.delete()  
        return redirect('perfil_list')  


def crear_seccion(request, perfil_pk, form_class=None):
    """
    Crea una sección asociada a un perfil específico.
    Recibe el formulario y el perfil.
    """
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

    return render(request, 'perfiles/form_seccion.html', {'form': form, 'perfil': perfil})


def actualizar_seccion(request, pk, model_class=None, form_class=None):
    """
    Edita una sección específica (experiencia, curso, producto, etc.).
    """
    obj = get_object_or_404(model_class, pk=pk)
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.perfil = obj.perfil  
            obj.save()
            return redirect('perfil_detail', pk=obj.perfil.pk)
    else:
        form = form_class(instance=obj)
    
    return render(request, 'perfiles/form_seccion.html', {'form': form, 'perfil': obj.perfil})


def eliminar_seccion(request, pk, model_class=None):
    """
    Elimina un registro de cualquier sección.
    """
    obj = get_object_or_404(model_class, pk=pk)
    perfil_pk = obj.perfil.pk  
    obj.delete()
    return redirect('perfil_detail', pk=perfil_pk)


def descargar_perfil(request, pk):
    """
    Genera un PDF del perfil completo con todas sus secciones activas.
    ⚠ Se agregaron configuraciones para que las imágenes locales funcionen correctamente.
    """
    perfil = get_object_or_404(DatosPersonales, pk=pk)

    html = render_to_string(
        'perfiles/pdf_perfil.html',
        {
            'perfil': perfil,
            'experiencias': ExperienciaLaboral.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'reconocimientos': Reconocimientos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'cursos': CursosRealizados.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'productos_academicos': ProductosAcademicos.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'productos_laborales': ProductosLaborales.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'ventas': VentaGarage.objects.filter(perfil=perfil, activarparaqueseveaenfront=True),
            'request': request, 
        }
    )

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {
        'enable-local-file-access': None, 
        'encoding': 'UTF-8',
        'quiet': ''
    }

    pdf = pdfkit.from_string(html, False, configuration=config, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{perfil.nombres}_{perfil.apellidos}.pdf"'
    return response
