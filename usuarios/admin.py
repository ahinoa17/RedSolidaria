from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nombre_completo', 'tipo_usuario', 'is_staff')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nombre_completo')
    ordering = ('email',)  # Cambiado de 'username' a 'email'
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('nombre_completo', 'telefono', 'tipo_usuario')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'tipo_usuario'),
        }),
    )
