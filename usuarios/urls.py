from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio
    path('registro/voluntario/', views.registro_voluntario, name='registro_voluntario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]