from django.shortcuts import render
from .models import EjercicioT
from .models import Entrenamiento
from .models import Serie

from .forms import EjercicioTForm
from .forms import EntrenamientoForm
from .forms import SerieForm
from .forms import TipoForm
from .forms import EmailForm
from .forms import EjercicioForm

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.shortcuts import redirect, get_object_or_404
# Create your views here.


def main(request):
    ejercicios = EjercicioT.objects.all()
    return render(request, 'myGymLog/mis_ejercicios.html', {'ejercicios':
                  ejercicios})


def nuevo_ejercicio(request):
    if request.method == "POST":
        form = EjercicioTForm(request.POST)
        if form.is_valid():
            ejercicio = form.save(commit=True)
            ejercicio.save()
            return redirect('main')
    else:
        form = EjercicioTForm()
    return render(request, 'myGymLog/anyadir_nuevo_ejercicio.html',
                  {'form': form})


def editar_ejercicio(request, pk):
    ejercicio = get_object_or_404(EjercicioT, pk=pk)
    if request.method == "POST":
        form = EjercicioTForm(request.POST, instance=ejercicio)
        if form.is_valid():
            ejercicio = form.save(commit=True)
            ejercicio.save()
            return redirect('main')
    else:
        form = EjercicioTForm(instance=ejercicio)
    return render(request, 'myGymLog/anyadir_nuevo_ejercicio.html',
                  {'form': form})

def crear_entrenamiento(request):
    if request.method == "POST":
        form = EntrenamientoForm(request.POST)
        if form.is_valid():
            entrenamiento = form.save(commit=False)
            entrenamiento.save()
            entr = Entrenamiento.objects.all().last()
            pk = entr.pk
            mostrar_ejercicio = True
            num_series_tonelaje = []


            return redirect('ejercicios', entr_pk=entr.pk)

    else:
        form = EntrenamientoForm()
        tipos=[]
        tipos.append("FullBody A")
        tipos.append("FullBody B")
        tipos.append("Weider Pecho")
        tipos.append("Torso")
        mostrar_ejercicio = False
        return render(request, 'myGymLog/crear_entrenamiento.html',
                  {'tipos':tipos, 'mostrar_ejercicio':mostrar_ejercicio, 'form':
                   form})

def listar_ejercicios(request,entr_pk):
    entr = Entrenamiento.objects.get(pk=entr_pk)
    if request.method == "POST":
        form = EjercicioForm(request.POST)
        if form.is_valid():
            ej= form.save(commit=False)
            nombre = ej.nombre
            ej = EjercicioT.objects.get(nombre=nombre)
            return redirect('series', entr_pk=entr.pk, ej_pk=ej.pk)
    else:
        form = EjercicioForm()
        lista = EjercicioT.objects.all()
        series = Serie.objects.filter(entrenamiento_id=entr_pk)
        listar_ejercicios =[]
        num_series = 1

        for ejercicio in lista:
            if series.filter(ejercicioT_id = ejercicio.pk):
                if ejercicio not in listar_ejercicios:
                    listar_ejercicios.append(ejercicio)
        listar_ejercicios = list(set(listar_ejercicios))
        num_series = []
        tonelaje = []
        lista_ej = []
        for ejercicio in listar_ejercicios:
            serie_aux = series.filter(ejercicioT_id = ejercicio.pk)
            num_series.append(len(serie_aux))
            tonelaje.append(series_tonelaje(serie_aux))
            lista_ej.append((ejercicio.nombre, len(serie_aux), series_tonelaje(serie_aux)))


        return render(request, 'myGymLog/listar_ejercicios.html',{'form':form
        ,'tipo':entr.tipo,'fecha':entr.fecha,'lista':lista,'entr_pk':entr_pk, 'listar_ejercicios':listar_ejercicios, 'num_series':num_series, 'tonelaje':tonelaje, 'lista_ej':lista_ej})


def lista_series(request, entr_pk, ej_pk):
    ej = EjercicioT.objects.get(pk = ej_pk)
    listar_series = Serie.objects.filter(entrenamiento_id = entr_pk)
    listar_series = listar_series.filter(ejercicioT_id = ej_pk)
    return render(request,'myGymLog/ver_series.html',{'listar_series':listar_series,'nombre':ej.nombre, 'entr_pk': entr_pk, 'ej_pk':ej_pk})


def serie_nueva(request, entr_pk, ej_pk):
    if request.method=="POST":
        form = SerieForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.entrenamiento_id = entr_pk
            serie.ejercicioT_id= ej_pk
            serie.save()
        return redirect('series',entr_pk=entr_pk, ej_pk=ej_pk)
    else:
        form = SerieForm()
        ej = EjercicioT.objects.get(pk = ej_pk)
        return render(request,'myGymLog/serie_nueva.html',{'nombre':ej.nombre, 'form':form})

def mis_entrenamientos(request):
    entrenamientos = Entrenamiento.objects.all()
    tipos = []
    for i in entrenamientos:
        tipo = i.tipo
        for j in tipos:
            if j == tipo:
                break
        else:
            tipos.append(tipo)
            tipo_seleccionado = 'Todos'
    if request.method == "POST":
        form = TipoForm(request.POST)
        entr = form.save(commit=False)
        tipo_seleccionado = entr.tipo
        entrenamientos = entrenamientos.filter(tipo = tipo_seleccionado)
    return render(request, 'myGymLog/mis_entrenamientos.html', {'entrenamientos':entrenamientos,
                    'tipos':tipos, 'tipo_seleccionado':tipo_seleccionado})


def anyadir_ejercicio(request, pk):
    ejercicio = get_object_or_404(EjercicioT, pk=pk)

    if request.method == "POST":
        form = SerieForm(request.POST)
        if form.is_valid():
            serie = form.save(commit=True)
            serie.fk = ejercicio.pk
            serie.save()
            lista = Serie.objects.filter(ejercicioT_id = pk)
            return render(request,'myGymLog/crear_entrenamiento.html', {
                'anyadir_serie':True, 'ejercicio':ejercicio , 'lista':lista})
    else:
        form = SerieForm()
        lista = Serie.objects.filter(ejercicioT_id = pk)


        return render(request,'myGymLog/crear_entrenamiento.html', {
            'anyadir_serie':True, 'ejercicio':ejercicio, 'lista':lista})

def series_tonelaje(series):
    tonelaje = 0
    for serie in series:
        tonelaje = tonelaje + serie.repeticiones * serie.peso
    return tonelaje

def crearUsuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form = EmailForm(request.POST)
            if form.is_valid():
                usuario_email = form.save(commit=False)
                user.email = usuario_email.email
                user.save()
    return render(request,'myGymLog/mis_ejercicios.html', {})
