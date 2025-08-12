from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    # Redirige la raíz al login
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Incluye las URLs de otras apps
    path('oportunidades/', include('oportunidades.urls')),
    path('organizaciones/', include('organizaciones.urls')),
    path('inscripciones/', include('inscripciones.urls')),
    path('permutaciones/', include('permutaciones.urls', namespace='permutaciones')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)