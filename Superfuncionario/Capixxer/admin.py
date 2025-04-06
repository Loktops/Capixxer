from django.contrib import admin
from .models import Loja, DadosLoja

@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'endereco', 'email')

@admin.register(DadosLoja)
class DadosLojaAdmin(admin.ModelAdmin):
    list_display = ('loja', 'data', 'vendas', 'clientes', 'ticket_medio', 'meta')
    list_filter = ('loja', 'data')
    search_fields = ('loja__nome', 'observacoes')
