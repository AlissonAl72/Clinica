from django.urls import path, include  # Garanta que 'include' está importado
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', include('core.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
