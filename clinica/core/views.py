from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *

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
      
        list_url_name = f"{self.object._meta.model_name}_list"
        context['cancel_url'] = reverse_lazy(list_url_name)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            context = self.get_context_data(object=self.object)
            context['error_message'] = f"Não é possível apagar '{self.object}', pois existem outros registos dependentes dele."
            return self.render_to_response(context)


def create_crud_views(model_class, form_class, list_template=None):
    model_name_lower = model_class._meta.model_name
    model_class_name = model_class.__name__
    list_view = type(f'{model_class_name}ListView', (LoginRequiredMixin, ListView), {'model': model_class, 'template_name': list_template or f'templates/core/{model_name_lower}_list.html'})
    create_view = type(f'{model_class_name}CreateView', (BaseCreateView,), {'model': model_class, 'form_class': form_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    update_view = type(f'{model_class_name}UpdateView', (BaseUpdateView,), {'model': model_class, 'form_class': form_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    delete_view = type(f'{model_class_name}DeleteView', (BaseDeleteView,), {'model': model_class, 'success_url': reverse_lazy(f'{model_name_lower}_list')})
    return list_view, create_view, update_view, delete_view

PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView = create_crud_views(Paciente, PacienteForm, list_template='templates/core/paciente_list.html')
MedicoListView, MedicoCreateView, MedicoUpdateView, MedicoDeleteView = create_crud_views(Medico, MedicoForm, list_template='templates/core/medico_list.html')
ConsultaListView, ConsultaCreateView, ConsultaUpdateView, ConsultaDeleteView = create_crud_views(Consulta, ConsultaForm, list_template='templates/core/consulta_list.html')
EspecialidadeListView, EspecialidadeCreateView, EspecialidadeUpdateView, EspecialidadeDeleteView = create_crud_views(Especialidade, EspecialidadeForm, list_template='templates/core/especialidade_list.html')
ConvenioListView, ConvenioCreateView, ConvenioUpdateView, ConvenioDeleteView = create_crud_views(Convenio, ConvenioForm, list_template='templates/core/convenio_list.html')
ExameListView, ExameCreateView, ExameUpdateView, ExameDeleteView = create_crud_views(Exame, ExameForm, list_template='templates/core/exame_list.html')
MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView = create_crud_views(Medicamento, MedicamentoForm, list_template='templates/core/medicamento_list.html')
PedidoExameListView, PedidoExameCreateView, PedidoExameUpdateView, PedidoExameDeleteView = create_crud_views(PedidoExame, PedidoExameForm, list_template='templates/core/pedidoexame_list.html')
PrescricaoListView, PrescricaoCreateView, PrescricaoUpdateView, PrescricaoDeleteView = create_crud_views(Prescricao, PrescricaoForm, list_template='templates/core/prescricao_list.html')

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
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
