# Importación del modelo Inscripcion
from .models import Inscripcion


def inscripciones_pendientes(request):
    """
    Procesador de contexto que agrega el conteo de inscripciones pendientes.
    
    Este procesador solo está disponible para superusuarios autenticados.
    Agrega al contexto la variable 'inscripciones_pendientes_count' que contiene
    el número total de inscripciones con estado 'pendiente'.
    
    Args:
        request: Objeto HttpRequest con la información de la petición.
        
    Returns:
        dict: Diccionario con el contexto actualizado o vacío si el usuario no es superusuario.
    """
    # Diccionario de contexto inicialmente vacío
    context = {}
    
    # Verifica si el usuario está autenticado y es superusuario
    if request.user.is_authenticated and request.user.is_superuser:
        # Cuenta las inscripciones pendientes y las agrega al contexto
        context['inscripciones_pendientes_count'] = Inscripcion.objects.filter(
            estado='pendiente'
        ).count()
    
    return context