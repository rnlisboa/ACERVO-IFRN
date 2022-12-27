from django.contrib import admin
from .models import *
class ProdutorAdmin(admin.ModelAdmin):
    list_display = ('nome_produtor',)
    
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome_categoria',)

class ObjetoAdmin(admin.ModelAdmin):
    list_display = ('titulo','autor',)

admin.site.register(Produtor, ProdutorAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Objeto, ObjetoAdmin)

# Register your models here.
