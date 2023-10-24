from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from sistema_integrado_notificaciones.models import Entidad, Comunicado


# Register your models here.

class ComunicadoAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        grupos_usuario = request.user.groups.all()
        primeraIteracion = True
        comunicados = None
        for grupo in grupos_usuario:
            if primeraIteracion:
                comunicados = super().get_queryset(request).filter(entidad__grupo_asociado = grupo)
                primeraIteracion = False
            else:
                comunicados = comunicados | super().get_queryset(request).filter(entidad__grupo_asociado = grupo)
        if comunicados == None:
            return super().get_queryset(request)
        return comunicados
    
    def formfield_for_foreignkey(self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any) -> ModelChoiceField | None:
        if db_field.name == 'entidad':
            grupos_usuario = [group.name for group in request.user.groups.all()]

            kwargs['queryset'] = Entidad.objects.filter(grupo_asociado__name__in = grupos_usuario)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)




admin.site.register(Entidad)
admin.site.register(Comunicado, ComunicadoAdmin)