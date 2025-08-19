# Importa el decorador user_passes_test de Django
from django.contrib.auth.decorators import user_passes_test

# Define un decorador personalizado para verificar superusuario
def superusuario_requerido(view_func):
    """
    Decorador que verifica si el usuario está autenticado y es superusuario.
    Si no cumple, redirige a la vista 'lista_organizaciones'.
    """
    # Aplica el decorador user_passes_test con una función lambda de verificación
    decorated_view = user_passes_test(
        # Función que verifica:
        # 1. Que el usuario esté autenticado
        # 2. Que sea superusuario
        lambda user: user.is_authenticated and user.is_superuser,
        
        # URL a la que redirigir si la verificación falla
        login_url='lista_organizaciones'
    )
    
    # Aplica el decorador a la vista y la devuelve
    return decorated_view(view_func)