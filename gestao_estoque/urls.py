# gestao_estoque/urls.py (NOVO ARQUIVO)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # RF4: Interface de autenticação de usuários (usa o LoginView nativo do Django com template customizado)
    path('login/', auth_views.LoginView.as_view(template_name='gestao_estoque/login.html'), name='login'),
    # RF5.1.2: Meio para o usuário fazer logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # RF5: Interface principal do sistema (Dashboard)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # RF6: Interface cadastro de produto
    path('cadastro_produto/', views.cadastro_produto_view, name='cadastro_produto'),
    
    # RF7: Interface gestão de estoque
    path('gestao_estoque/', views.gestao_estoque_view, name='gestao_estoque'),
]