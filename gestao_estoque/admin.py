# Arquivo: gestao_estoque/admin.py

from django.contrib import admin
from .models import Produto, MovimentacaoEstoque

# Customização da MovimentacaoEstoque
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo_movimentacao', 'quantidade', 'data_movimentacao', 'usuario')
    list_filter = ('tipo_movimentacao', 'produto')
    search_fields = ('produto__nome',)
    # RF7.1.3 CORREÇÃO: 'data_movimentacao' foi removida para permitir inserção manual.
    readonly_fields = () 
    
# Customização do Produto
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estoque_atual', 'estoque_minimo', 'descricao')
    list_filter = ('estoque_minimo',)
    search_fields = ('nome', 'descricao') # RF6.1.2: Campo de busca

# Registra os Models (Cria as interfaces no Admin)
admin.site.register(Produto, ProdutoAdmin) # RF6: Cadastro de Produto
admin.site.register(MovimentacaoEstoque, MovimentacaoEstoqueAdmin) # RF7: Gestão de Estoque