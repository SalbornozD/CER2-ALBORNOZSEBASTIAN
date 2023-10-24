from django.db import models
from django.contrib.auth.models import Group


class Entidad(models.Model):
    id = models.BigAutoField(primary_key= True)
    nombre = models.CharField(max_length=30)
    logo = models.ImageField(upload_to="logos", null=True)
    grupo_asociado = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.nombre
    

class Comunicado(models.Model):
    TIPO_CHOICES = [
        ("S", "Suspención de actividades"),
        ("C", "Suspención de clases"),
        ("I", "Información")]

    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=30)
    detalle = models.CharField(max_length=500)
    detalle_corto = models.CharField(max_length=200)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    entidad = models.ForeignKey(Entidad, on_delete = models.CASCADE)
    visible = models.BooleanField()
    fecha_publicacion = models.DateTimeField()
    fecha_ultima_modificacion = models.DateTimeField()
    

    def __str__(self) -> str:
        return self.titulo