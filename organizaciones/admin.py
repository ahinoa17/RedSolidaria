from django.contrib import admin
from .models import Organizacion

@admin.register(Organizacion)
class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'contacto_email', 'telefono', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'contacto_email')
    fields = ('nombre', 'descripcion', 'contacto_email', 'telefono', 'direccion', 'logo', 'activa')
