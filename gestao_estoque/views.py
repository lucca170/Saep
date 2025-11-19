# gestao_estoque/views.py (MODIFICADO)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produto, MovimentacaoEstoque
from django.db.models import Q # Importa Q para buscas com OR

# RF5: Interface principal do sistema (Dashboard)
@login_required
def dashboard_view(request):
    user = request.user # RF5.1.1: Exibir nome do usuário logado
    context = {
        'user': user
    }
    return render(request, 'gestao_estoque/dashboard.html', context)

# RF6: Interface cadastro de produto
@login_required
def cadastro_produto_view(request):
    # RF6.1.1: Listar os produtos cadastrados
    produtos = Produto.objects.all()
    
    # Lógica de Busca (RF6.1.2)
    search_query = request.GET.get('q')
    if search_query:
        # Busca por nome OU descrição
        produtos = produtos.filter(
            Q(nome__icontains=search_query) | Q(descricao__icontains=search_query)
        )

    context = {
        'produtos': produtos,
        'search_query': search_query
    }
    return render(request, 'gestao_estoque/cadastro_produto.html', context)

# RF7: Interface gestão de estoque
@login_required
def gestao_estoque_view(request):
    # RF7.1.1: Listar produtos cadastrados em ordem alfabética (Algoritmo de ordenação via ORM)
    produtos_ordenados = Produto.objects.all().order_by('nome') 
    
    # Lista as 10 últimas movimentações registradas
    movimentacoes = MovimentacaoEstoque.objects.all().order_by('-data_movimentacao')[:10]

    context = {
        'produtos': produtos_ordenados,
        'movimentacoes': movimentacoes
    }
    return render(request, 'gestao_estoque/gestao_estoque.html', context)