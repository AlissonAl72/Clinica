from django import forms
from .models import *

class EspecialidadeForm(forms.ModelForm):
    class Meta:
        model = Especialidade
        fields = ['nome']

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome_completo', 'crm', 'especialidade', 'telefone']

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ['nome', 'codigo_ans']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome_completo', 'data_nascimento', 'cpf', 'convenio']
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'})}

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data_hora', 'status']
        widgets = {'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ['historico_medico']

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['nome', 'descricao', 'custo']

class PedidoExameForm(forms.ModelForm):
    class Meta:
        model = PedidoExame
        fields = ['consulta', 'exame', 'realizado', 'resultado_disponivel']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome_comercial', 'principio_ativo', 'fabricante']

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ['consulta', 'medicamento', 'posologia']