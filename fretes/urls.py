from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('selecionar-origem/', views.selecionar_origem, name='selecionar_origem'),
    path('selecionar-destino/', views.selecionar_destino, name='selecionar_destino'),
    path('loja-info/<int:loja_id>/', views.loja_info, name='loja_info'),
    path('meus-fretes/', views.meus_fretes, name='meus_fretes'),
    path('frete/<int:frete_id>/', views.frete_detalhe, name='frete_detalhe'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='fretes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', views.home, name='home'),
]
