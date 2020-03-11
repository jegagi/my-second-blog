from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('ejercicio/nuevo', views.nuevo_ejercicio, name='nuevo_ejercicio'),
    path('ejercicio/<int:pk>/editar/', views.editar_ejercicio,
         name='editar_ejercicio'),
    path('ejercicio/crear_entrenamiento', views.crear_entrenamiento, name='crear_entrenamiento'),
    path('ejercicio/mis_entrenamientos', views.mis_entrenamientos, name='mis_entrenamientos'),
    path('ejercicio/mis_ejercicios', views.crearUsuario, name='crear'),
    path('series/<int:entr_pk>/<int:ej_pk>',views.lista_series,name='series'),
    path('listar_ejercicios/<int:entr_pk>',views.listar_ejercicios,name='ejercicios'),
    path('serie_nueva/<int:entr_pk>/<int:ej_pk>',views.serie_nueva,name='serie_nueva'),
]
