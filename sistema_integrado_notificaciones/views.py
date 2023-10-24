from django.shortcuts import render
from sistema_integrado_notificaciones.models import Comunicado, Entidad

# Create your views here.

def index(request):
    entidad = request.GET.get("entidad", "Todas")
    comunicados = list((Comunicado.objects.all().filter(visible = True)).order_by('-fecha_publicacion'))
    entidades = list(Entidad.objects.all())
    if entidad == "Todas":
        entidades.insert(0, "Todas")
        contexto = {"comunicados": comunicados, "entidades": entidades}
    else:
        for i in entidades:
            if i.nombre == entidad:
                entidades.remove(i)
                entidades.insert(0, i)
                
        entidades.append("Todas")
        comunicados = list(((Comunicado.objects.all().filter(entidad__nombre = entidad)).filter(visible = True)).order_by('-fecha_publicacion'))
        contexto = {"comunicados": comunicados, "entidades": entidades, "entidad": entidad}

    return render(request, 'sistema_integrado_notificaciones/index.html', contexto)
