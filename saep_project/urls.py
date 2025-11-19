# saep_project/urls.py (MODIFICADO)

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    # Redireciona a raiz (/) para o login se não autenticado, ou para o dashboard se autenticado.
    path('', lambda request: redirect('login') if not request.user.is_authenticated else redirect('dashboard'), name='root'),
    
    # Rota do Django Admin
    path('admin/', admin.site.urls),
    
    # Inclui as URLs da aplicação gestao_estoque
    path('', include('gestao_estoque.urls')),
]