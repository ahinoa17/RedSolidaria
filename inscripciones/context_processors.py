from .models import Inscripcion

def inscripciones_pendientes(request):
    context = {}
    if request.user.is_authenticated and request.user.is_superuser:
        context['inscripciones_pendientes_count'] = Inscripcion.objects.filter(estado='pendiente').count()
    return context
