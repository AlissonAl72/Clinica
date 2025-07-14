from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class HomeView(LoginRequiredMixin, ListView):
    model = Consulta
    template_name = 'core/home.html'
    context_object_name = 'consultas'
    ordering = ['-data_hora']


class BaseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'core/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name
        return context

class BaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/generic_form.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.object._meta.verbose_name
        return context

class BaseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'core/generic_confirm_delete.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.object._meta.verbose_name
        context['cancel_url'] = self.request.META.get('HTTP_REFERER', self.success_url)
        return context

def create_crud_views(model_class, form_class, list_template=None):
    model_name_lower = model_class._meta.model_name
    model_class_name = model_class.__name__
    list_view = type(f'{model_class_name}ListView', (LoginRequiredMixin, ListView), {'model': model_class, 'template_name': list_template or f'core/{model_name_lower}_list.html'})
    create_view = type(f'{model_class_name}CreateView', (BaseCreateView,), {'model': model_class, 'form_class': form_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    update_view = type(f'{model_class_name}UpdateView', (BaseUpdateView,), {'model': model_class, 'form_class': form_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    delete_view = type(f'{model_class_name}DeleteView', (BaseDeleteView,), {'model': model_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    return list_view, create_view, update_view, delete_view

PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView = create_crud_views(Paciente, PacienteForm)
MedicoListView, MedicoCreateView, MedicoUpdateView, MedicoDeleteView = create_crud_views(Medico, MedicoForm)
ConsultaListView, ConsultaCreateView, ConsultaUpdateView, ConsultaDeleteView = create_crud_views(Consulta, ConsultaForm)
EspecialidadeListView, EspecialidadeCreateView, EspecialidadeUpdateView, EspecialidadeDeleteView = create_crud_views(Especialidade, EspecialidadeForm)
ConvenioListView, ConvenioCreateView, ConvenioUpdateView, ConvenioDeleteView = create_crud_views(Convenio, ConvenioForm)
ExameListView, ExameCreateView, ExameUpdateView, ExameDeleteView = create_crud_views(Exame, ExameForm)
MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView = create_crud_views(Medicamento, MedicamentoForm)
PedidoExameListView, PedidoExameCreateView, PedidoExameUpdateView, PedidoExameDeleteView = create_crud_views(PedidoExame, PedidoExameForm)
PrescricaoListView, PrescricaoCreateView, PrescricaoUpdateView, PrescricaoDeleteView = create_crud_views(Prescricao, PrescricaoForm)

class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'core/paciente_detail.html'

class ProntuarioUpdateView(BaseUpdateView):
    model = Prontuario
    form_class = ProntuarioForm
    template_name = 'core/prontuario_form.html'
    def get_success_url(self):
        return reverse_lazy('paciente_detail', kwargs={'pk': self.object.pk})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login') # Redireciona para a página de login após o registo
    template_name = 'registration/signup.html'