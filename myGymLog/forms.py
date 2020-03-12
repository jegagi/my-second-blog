from django import forms

from .models import EjercicioT, Entrenamiento, Serie
from django.contrib.auth.models import User


class EjercicioTForm(forms.ModelForm):

    class Meta:
        model = EjercicioT
        fields = ('nombre', 'musculoPrincipal', 'musculoSecundario1',
                  'musculoSecundario2', 'musculoSecundario3')


class EntrenamientoForm(forms.ModelForm):

    class Meta:
        model = Entrenamiento
        widgets = {
            'fecha': forms.DateInput(
                format='%d/%m/%Y',
                attrs={'class': 'form-control datepicker',
                       'autocomplete': 'off','id':'datepicker'}
            )
        }
        fields = ('fecha', 'tipo')


class SerieForm(forms.ModelForm):

    class Meta:
        model = Serie
        fields = ('repeticiones', 'peso', 'rir', 'observaciones')


class TipoForm(forms.ModelForm):

    class Meta:
        model = Entrenamiento
        fields = ('tipo',)


class EjercicioForm(forms.ModelForm):

    class Meta:
        model = EjercicioT
        fields = ('nombre',)


class EmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)
