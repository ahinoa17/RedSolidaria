# Importa el módulo admin de Django
from django.contrib import admin

# Importa el modelo Organizacion del directorio actual
from .models import Organizacion

# Registra el modelo Organizacion en el panel de administración
# y lo personaliza con la clase OrganizacionAdmin
@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de organizaciones
    list_display = ('nombre', 'contacto_email', 'telefono', 'activa')
    
    # Filtros que aparecerán en la barra lateral
    list_filter = ('activa',)
    
    # Campos por los que se podrá buscar
    search_fields = ('nombre', 'contacto_email')
    
    # Orden y agrupación de campos en el formulario de edición
    fields = ('nombre', 'descripcion', 'contacto_email', 
             'telefono', 'direccion', 'logo', 'activa')