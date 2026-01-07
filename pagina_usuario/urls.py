from django.urls import path
from functools import partial
from .views import (
    PerfilListView,
    PerfilDetailView,
    PerfilCreateView,
    PerfilUpdateView,
    PerfilDeleteView,
    descargar_perfil,
    crear_seccion,
    actualizar_seccion,
    eliminar_seccion,
)
from .models import (
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)
from .forms import (
    ExperienciaLaboralForm,
    ReconocimientosForm,
    CursosRealizadosForm,
    ProductosAcademicosForm,
    ProductosLaboralesForm,
    VentaGarageForm
)

experiencia_create_view = partial(crear_seccion, form_class=ExperienciaLaboralForm)
experiencia_update_view = partial(actualizar_seccion, model_class=ExperienciaLaboral, form_class=ExperienciaLaboralForm)
experiencia_delete_view = partial(eliminar_seccion, model_class=ExperienciaLaboral)

reconocimiento_create_view = partial(crear_seccion, form_class=ReconocimientosForm)
reconocimiento_update_view = partial(actualizar_seccion, model_class=Reconocimientos, form_class=ReconocimientosForm)
reconocimiento_delete_view = partial(eliminar_seccion, model_class=Reconocimientos)

curso_create_view = partial(crear_seccion, form_class=CursosRealizadosForm)
curso_update_view = partial(actualizar_seccion, model_class=CursosRealizados, form_class=CursosRealizadosForm)
curso_delete_view = partial(eliminar_seccion, model_class=CursosRealizados)

producto_academico_create_view = partial(crear_seccion, form_class=ProductosAcademicosForm)
producto_academico_update_view = partial(actualizar_seccion, model_class=ProductosAcademicos, form_class=ProductosAcademicosForm)
producto_academico_delete_view = partial(eliminar_seccion, model_class=ProductosAcademicos)

producto_laboral_create_view = partial(crear_seccion, form_class=ProductosLaboralesForm)
producto_laboral_update_view = partial(actualizar_seccion, model_class=ProductosLaborales, form_class=ProductosLaboralesForm)
producto_laboral_delete_view = partial(eliminar_seccion, model_class=ProductosLaborales)

venta_create_view = partial(crear_seccion, form_class=VentaGarageForm)
venta_update_view = partial(actualizar_seccion, model_class=VentaGarage, form_class=VentaGarageForm)
venta_delete_view = partial(eliminar_seccion, model_class=VentaGarage)

urlpatterns = [
    path('', PerfilListView.as_view(), name='perfil_list'),
    path('crear/', PerfilCreateView.as_view(), name='perfil_create'),
    path('<int:pk>/', PerfilDetailView.as_view(), name='perfil_detail'),
    path('<int:pk>/editar/', PerfilUpdateView.as_view(), name='perfil_update'),
    path('<int:pk>/eliminar/', PerfilDeleteView.as_view(), name='perfil_delete'),
    path('<int:pk>/descargar/', descargar_perfil, name='descargar_perfil'),

    path('<int:perfil_pk>/experiencia/crear/', experiencia_create_view, name='experiencia_create'),
    path('experiencia/<int:pk>/editar/', experiencia_update_view, name='experiencia_update'),
    path('experiencia/<int:pk>/eliminar/', experiencia_delete_view, name='experiencia_delete'),

    path('<int:perfil_pk>/reconocimiento/crear/', reconocimiento_create_view, name='reconocimiento_create'),
    path('reconocimiento/<int:pk>/editar/', reconocimiento_update_view, name='reconocimiento_update'),
    path('reconocimiento/<int:pk>/eliminar/', reconocimiento_delete_view, name='reconocimiento_delete'),

    path('<int:perfil_pk>/curso/crear/', curso_create_view, name='curso_create'),
    path('curso/<int:pk>/editar/', curso_update_view, name='curso_update'),
    path('curso/<int:pk>/eliminar/', curso_delete_view, name='curso_delete'),

    path('<int:perfil_pk>/producto_academico/crear/', producto_academico_create_view, name='producto_academico_create'),
    path('producto_academico/<int:pk>/editar/', producto_academico_update_view, name='producto_academico_update'),
    path('producto_academico/<int:pk>/eliminar/', producto_academico_delete_view, name='producto_academico_delete'),

    path('<int:perfil_pk>/producto_laboral/crear/', producto_laboral_create_view, name='producto_laboral_create'),
    path('producto_laboral/<int:pk>/editar/', producto_laboral_update_view, name='producto_laboral_update'),
    path('producto_laboral/<int:pk>/eliminar/', producto_laboral_delete_view, name='producto_laboral_delete'),

    path('<int:perfil_pk>/venta/crear/', venta_create_view, name='venta_create'),
    path('venta/<int:pk>/editar/', venta_update_view, name='venta_update'),
    path('venta/<int:pk>/eliminar/', venta_delete_view, name='venta_delete'),
]
