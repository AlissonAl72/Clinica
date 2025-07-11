from django.db import models

# Create your models here.

# core/models.py
from django.db import models
from django.contrib.auth.models import User

# Entidade 1: Especialidade Médica
class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Ex: Cardiologia, Neurologia")

    def __str__(self):
        return self.nome

# Entidade 2: Médico
class Medico(models.Model):
    nome_completo = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, unique=True, help_text="Conselho Regional de Medicina")
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name="medicos")
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nome_completo} ({self.especialidade.nome})"

# Entidade 3: Convênio Médico
class Convenio(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    codigo_ans = models.CharField(max_length=50, unique=True, help_text="Registro na Agência Nacional de Saúde")

    def __str__(self):
        return self.nome

# Entidade 4: Paciente
class Paciente(models.Model):
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    convenio = models.ForeignKey(Convenio, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.nome_completo

# Entidade 5: Consulta
class Consulta(models.Model):
    STATUS_CHOICES = [
        ('AGENDADA', 'Agendada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="consultas")
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AGENDADA')

    def __str__(self):
        return f"Consulta de {self.paciente.nome_completo} com {self.medico.nome_completo} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

# Entidade 6: Prontuário
class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, primary_key=True)
    historico_medico = models.TextField(blank=True, help_text="Histórico de doenças, alergias, etc.")
    
    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo}"

# Entidade 7: Exame
class Exame(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

# Entidade 8: Pedido de Exame
class PedidoExame(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="pedidos_exames")
    exame = models.ForeignKey(Exame, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now_add=True)
    realizado = models.BooleanField(default=False)
    resultado_disponivel = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido de {self.exame.nome} para {self.consulta.paciente.nome_completo}"

# Entidade 9: Medicamento
class Medicamento(models.Model):
    nome_comercial = models.CharField(max_length=100)
    principio_ativo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_comercial

# Entidade 10: Prescrição
class Prescricao(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="prescricoes")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    posologia = models.TextField(help_text="Instruções de uso. Ex: 1 comprimido a cada 8 horas por 7 dias.")
    data_prescricao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescrição de {self.medicamento.nome_comercial} para {self.consulta.paciente.nome_completo}"


