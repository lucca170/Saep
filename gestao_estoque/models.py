from django.db import models
from django.contrib.auth.models import User 

# Tabela 1: Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    estoque_atual = models.IntegerField(default=0, verbose_name="Estoque Atual")
    estoque_minimo = models.IntegerField(default=5, verbose_name="Estoque Mínimo")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        
# Tabela 2: MovimentacaoEstoque
class MovimentacaoEstoque(models.Model):
    TIPO_MOVIMENTACAO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    tipo_movimentacao = models.CharField(max_length=1, choices=TIPO_MOVIMENTACAO_CHOICES, verbose_name="Tipo")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    data_movimentacao = models.DateField(auto_now_add=True, verbose_name="Data da Movimentação")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    def __str__(self):
        return f"{self.get_tipo_movimentacao_display()} de {self.quantidade} de {self.produto.nome}"
    
    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']