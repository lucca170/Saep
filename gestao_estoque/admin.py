from django.contrib import admin
from django.contrib import messages
from .models import Produto, MovimentacaoEstoque

# Customização da MovimentacaoEstoque
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo_movimentacao', 'quantidade', 'data_movimentacao', 'usuario')
    list_filter = ('tipo_movimentacao', 'produto')
    search_fields = ('produto__nome',)
    readonly_fields = ('data_movimentacao', 'usuario') 

    # Implementação da Lógica de Estoque e Validação (RF7.1.4, RF12)
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Define o usuário logado na criação
            obj.usuario = request.user
            
        produto = obj.produto
        
        if obj.tipo_movimentacao == 'E': # Entrada
            produto.estoque_atual += obj.quantidade
        
        elif obj.tipo_movimentacao == 'S': # Saída
            # RF12: Validação para evitar estoque negativo
            if produto.estoque_atual < obj.quantidade:
                messages.error(request, f'ERRO: Saída ({obj.quantidade}) excede o estoque atual ({produto.estoque_atual})!')
                return # Impede de salvar a movimentação
            
            produto.estoque_atual -= obj.quantidade
            
        # Salva a Movimentação e atualiza o Produto
        super().save_model(request, obj, form, change)
        produto.save()
        
        # RF7.1.4: Alerta de Estoque Mínimo após Saída
        if obj.tipo_movimentacao == 'S' and produto.estoque_atual < produto.estoque_minimo:
            messages.warning(request, f'ATENÇÃO: O estoque de {produto.nome} ({produto.estoque_atual}) está ABAIXO do mínimo configurado ({produto.estoque_minimo}).')

# Customização do Produto
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estoque_atual', 'estoque_minimo', 'descricao')
    list_filter = ('estoque_minimo',)
    search_fields = ('nome', 'descricao') # RF6.1.2: Campo de busca

# Registra os Models (Cria as interfaces no Admin)
admin.site.register(Produto, ProdutoAdmin) # RF6: Cadastro de Produto
admin.site.register(MovimentacaoEstoque, MovimentacaoEstoqueAdmin) # RF7: Gestão de Estoque