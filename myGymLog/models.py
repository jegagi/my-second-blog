from django.db import models

# Create your models here.


class EjercicioT(models.Model):
    nombre = models.CharField(max_length=20)
    musculoPrincipal = models.CharField(max_length=20)
    musculoSecundario1 = models.CharField(max_length=20)
    musculoSecundario2 = models.CharField(max_length=20, blank=True, null=True)
    musculoSecundario3 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Serie(models.Model):
    repeticiones = models.IntegerField()
    peso = models.DecimalField(max_digits=4,decimal_places=1)
    rir = models.IntegerField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    ejercicioT = models.ForeignKey(
        'EjercicioT',
        on_delete = models.CASCADE,
        default = '0'
    )
    entrenamiento = models.ForeignKey(
        'Entrenamiento',
        on_delete=models.CASCADE,
        default = '0'
    )

    def calc_tonelaje(self):
        return self.peso*self.repeticiones

    def __repr__(self):
        return self.repeticiones + " x " + self.peso



class Entrenamiento(models.Model):
    fecha = models.DateField()
    tipo = models.CharField(max_length=20)
