# Arquivo: gestao_estoque/models.py

from django.db import models
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError # NOVO
from django.db.models.signals import post_save # NOVO
from django.dispatch import receiver # NOVO

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
    # RF7.1.3 CORREÇÃO: Removido auto_now_add=True
    data_movimentacao = models.DateField(verbose_name="Data da Movimentação")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    # RF6.1.6: Validações (Quantidade e Estoque Suficiente)
    def clean(self):
        # 1. Validação: Quantidade positiva
        if self.quantidade <= 0:
             raise ValidationError({'quantidade': 'A quantidade deve ser um valor positivo para a movimentação.'})
             
        # 2. Validação: Não permite saída maior que o estoque atual
        if self.tipo_movimentacao == 'S':
            produto_atual = Produto.objects.get(pk=self.produto.pk) 
            if self.quantidade > produto_atual.estoque_atual:
                raise ValidationError(f"Não há estoque suficiente para a saída. Estoque atual: {produto_atual.estoque_atual}.")

    def __str__(self):
        return f"{self.get_tipo_movimentacao_display()} de {self.quantidade} de {self.produto.nome}"
    
    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']
        
# RF7.1.4 Lógica: Signal para atualização automática do estoque e checagem de alerta
@receiver(post_save, sender=MovimentacaoEstoque)
def update_stock_and_check_min(sender, instance, created, **kwargs):
    if created: # Apenas quando uma nova movimentação for criada
        produto = instance.produto
        
        # 1. Atualiza o Estoque
        if instance.tipo_movimentacao == 'E':
            produto.estoque_atual += instance.quantidade
        elif instance.tipo_movimentacao == 'S':
            produto.estoque_atual -= instance.quantidade

        # 2. RF7.1.4: Implementa a verificação automática de estoque mínimo (Alerta)
        if produto.estoque_atual < produto.estoque_minimo:
            # Em ambiente de teste, o alerta é gerado no console do servidor.
            print(f"ALERTA RF7.1.4: Produto '{produto.nome}' está abaixo do estoque mínimo ({produto.estoque_minimo}). Estoque atual: {produto.estoque_atual}") 

        produto.save()