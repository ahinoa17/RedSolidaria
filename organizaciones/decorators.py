from django.contrib.auth.decorators import user_passes_test

def superusuario_requerido(view_func):
    decorated_view = user_passes_test(
        lambda user: user.is_authenticated and user.is_superuser,
        login_url='lista_organizaciones'
    )
    return decorated_view(view_func)