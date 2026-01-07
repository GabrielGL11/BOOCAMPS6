from django import forms
from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimientos,
    CursosRealizados,
    ProductosAcademicos,
    ProductosLaborales,
    VentaGarage
)

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = '__all__'
        widgets = {
            'fechanacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        exclude = ('perfil',)
        widgets = {
            'fechainiciogestion': forms.DateInput(attrs={'type': 'date'}),
            'fechafingestion': forms.DateInput(attrs={'type': 'date'}),
        }

class ReconocimientosForm(forms.ModelForm):
    class Meta:
        model = Reconocimientos
        exclude = ('perfil',)
        widgets = {
            'fechareconocimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class CursosRealizadosForm(forms.ModelForm):
    class Meta:
        model = CursosRealizados
        exclude = ('perfil',)
        widgets = {
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
        }

class ProductosAcademicosForm(forms.ModelForm):
    class Meta:
        model = ProductosAcademicos
        exclude = ('perfil',)

class ProductosLaboralesForm(forms.ModelForm):
    class Meta:
        model = ProductosLaborales
        exclude = ('perfil',)
        widgets = {
            'fechaproducto': forms.DateInput(attrs={'type': 'date'}),
        }

class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        exclude = ('perfil',)
