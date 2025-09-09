from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ...existing code...
    path('frete/<int:frete_id>/atualizar-status/', views.atualizar_status_frete, name='atualizar_status_frete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('selecionar-origem/', views.selecionar_origem, name='selecionar_origem'),
    path('selecionar-destino/', views.selecionar_destino, name='selecionar_destino'),
    path('loja-info/<int:loja_id>/', views.loja_info, name='loja_info'),
    path('meus-fretes/', views.meus_fretes, name='meus_fretes'),
    path('meus-fretes/relatorio-excel/', views.meus_fretes_relatorio_excel, name='meus_fretes_relatorio_excel'),
    path('frete/<int:frete_id>/', views.frete_detalhe, name='frete_detalhe'),
    path('frete/<int:frete_id>/editar/', views.editar_frete, name='editar_frete'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='fretes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('health/', views.health_check, name='health_check'),
    path('', views.home, name='home'),
    path('solicitar-frete/', views.selecionar_origem, name='solicitar_frete'),
]
