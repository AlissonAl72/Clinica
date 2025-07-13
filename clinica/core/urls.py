from django.urls import path
from . import views
from . import models

def create_crud_urls(model_class):
    model_name_lower = model_class._meta.model_name
    model_class_name = model_class.__name__
    list_view = getattr(views, f'{model_class_name}ListView')
    create_view = getattr(views, f'{model_class_name}CreateView')
    update_view = getattr(views, f'{model_class_name}UpdateView')
    delete_view = getattr(views, f'{model_class_name}DeleteView')
    return [
        path(f'{model_name_lower}s/', list_view.as_view(), name=f'{model_name_lower}_list'),
        path(f'{model_name_lower}s/novo/', create_view.as_view(), name=f'{model_name_lower}_create'),
        path(f'{model_name_lower}s/<int:pk>/editar/', update_view.as_view(), name=f'{model_name_lower}_update'),
        path(f'{model_name_lower}s/<int:pk>/apagar/', delete_view.as_view(), name=f'{model_name_lower}_delete'),
    ]

urlpatterns = [
    # A URL de signup foi ADICIONADA AQUI.
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('', views.HomeView.as_view(), name='home'),
    path('pacientes/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('prontuarios/<int:pk>/editar/', views.ProntuarioUpdateView.as_view(), name='prontuario_update'),
]

urlpatterns += create_crud_urls(models.Paciente)
urlpatterns += create_crud_urls(models.Medico)
urlpatterns += create_crud_urls(models.Consulta)
urlpatterns += create_crud_urls(models.Especialidade)
urlpatterns += create_crud_urls(models.Convenio)
urlpatterns += create_crud_urls(models.Exame)
urlpatterns += create_crud_urls(models.Medicamento)
urlpatterns += create_crud_urls(models.PedidoExame)
urlpatterns += create_crud_urls(models.Prescricao)
