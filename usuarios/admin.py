# Importaciones estándar de Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Importación del modelo personalizado de Usuario
from .models import Usuario


# Registro del modelo Usuario en el panel de administración
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración personalizada para el modelo Usuario en el admin de Django.
    Hereda de UserAdmin para personalizar la interfaz de administración.
    """
    
    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'nombre_completo', 'tipo_usuario', 'is_staff', 'acceso_admin')
    list_editable = ('acceso_admin',)
    
    # Filtros disponibles en el panel lateral
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser')
    
    # Campos por los que se puede buscar
    search_fields = ('email', 'nombre_completo')
    
    # Campos de solo lectura (útil para ver información sin modificar)
    readonly_fields = ('date_joined', 'last_login')
    
    def save_model(self, request, obj, form, change):
        # Guardar el modelo (la lógica de permisos está en el modelo)
        super().save_model(request, obj, form, change)
        
        # Actualizar los permisos del usuario
        from django.contrib.auth.models import Group
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        
        if obj.acceso_admin and not obj.is_superuser:
            obj.groups.add(admin_group)
            obj.is_staff = True
            # Asegurarse de que el usuario tenga los permisos del grupo
            obj.user_permissions.set(admin_group.permissions.all())
            obj.save(update_fields=['is_staff'])  # Solo actualizar el campo is_staff
        elif not obj.acceso_admin and not obj.is_superuser:
            obj.groups.remove(admin_group)
            obj.is_staff = False
            obj.save(update_fields=['is_staff'])  # Solo actualizar el campo is_staff
        
        # No mostrar mensajes aquí para evitar duplicación
        # Los mensajes se manejan en la vista editar_usuario
    
    # Ordenamiento por defecto (cambiado de 'username' a 'email')
    ordering = ('email',)
    
    # Configuración de los campos en el formulario de edición
    fieldsets = (
        # Sección básica (sin título)
        (None, {
            'fields': ('email', 'password')
        }),
        
        # Sección de información personal
        (_('Información personal'), {
            'fields': ('nombre_completo', 'telefono', 'tipo_usuario')
        }),
        
        # Sección de permisos y grupos
        (_('Permisos'), {
            'fields': (
                'is_active',
                'acceso_admin',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        
        # Sección de fechas importantes (último inicio de sesión, fecha de registro)
        (_('Fechas importantes'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)  # Permite colapsar esta sección
        }),
    )
    
    # Configuración de los campos en el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Clase CSS para un formulario más ancho
            'fields': (
                'email', 
                'password1', 
                'password2', 
                'tipo_usuario'  # Campo personalizado para el tipo de usuario
            ),
        }),
    )
