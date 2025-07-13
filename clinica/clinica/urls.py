from django.urls import path, include  # Garanta que 'include' está importado
from django.contrib.auth import views as auth_views

urlpatterns = [
    # CORREÇÃO PRINCIPAL: Esta linha inclui todas as URLs da sua aplicação 'core'.
    # Agora, o Django saberá o que fazer quando alguém aceder à página inicial.
    path('', include('core.urls')),

    # As URLs de autenticação que você já tinha.
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
