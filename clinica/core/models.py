from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Entidade 1: Especialidade Médica
class Especialidade(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Ex: Cardiologia, Neurologia")

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"

# Entidade 2: Médico
class Medico(models.Model):
    nome_completo = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, unique=True, help_text="Conselho Regional de Medicina")
    # Protegido: Não se pode apagar uma especialidade se houver médicos nela.
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, related_name="medicos")
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nome_completo} ({self.especialidade.nome})"

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

# Entidade 3: Convénio Médico
class Convenio(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    codigo_ans = models.CharField(max_length=50, unique=True, help_text="Registo na Agência Nacional de Saúde")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Convénio"
        verbose_name_plural = "Convénios"

# Entidade 4: Paciente
class Paciente(models.Model):
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    # Protegido: Não se pode apagar um convénio se houver pacientes nele.
    convenio = models.ForeignKey(Convenio, on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

# Entidade 5: Consulta
class Consulta(models.Model):
    STATUS_CHOICES = [('AGENDADA', 'Agendada'), ('REALIZADA', 'Realizada'), ('CANCELADA', 'Cancelada')]
    # Protegido: Não se pode apagar um paciente se ele tiver consultas.
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="consultas")
    # Protegido: Não se pode apagar um médico se ele tiver consultas.
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name="consultas")
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='AGENDADA')

    def __str__(self):
        return f"Consulta de {self.paciente.nome_completo} com {self.medico.nome_completo} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

# Entidade 6: Prontuário
class Prontuario(models.Model):
    # Protegido: Não se pode apagar um paciente se ele tiver um prontuário (neste caso, é OneToOne, mas a proteção é boa prática).
    paciente = models.OneToOneField(Paciente, on_delete=models.PROTECT, primary_key=True)
    historico_medico = models.TextField(blank=True, help_text="Histórico de doenças, alergias, etc.")
    
    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo}"

    class Meta:
        verbose_name = "Prontuário"
        verbose_name_plural = "Prontuários"

@receiver(post_save, sender=Paciente)
def criar_prontuario_paciente(sender, instance, created, **kwargs):
    if created:
        Prontuario.objects.create(paciente=instance)

# Entidade 7: Exame
class Exame(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"

# Entidade 8: Pedido de Exame
class PedidoExame(models.Model):
    # Protegido: Não se pode apagar uma consulta se houver pedidos de exame para ela.
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT, related_name="pedidos_exames")
    # Protegido: Não se pode apagar um tipo de exame se ele já foi pedido.
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT)
    data_pedido = models.DateField(auto_now_add=True)
    realizado = models.BooleanField(default=False)
    resultado_disponivel = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido de {self.exame.nome} para {self.consulta.paciente.nome_completo}"

    class Meta:
        verbose_name = "Pedido de Exame"
        verbose_name_plural = "Pedidos de Exames"

# Entidade 9: Medicamento
class Medicamento(models.Model):
    nome_comercial = models.CharField(max_length=100)
    principio_ativo = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_comercial

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

# Entidade 10: Prescrição
class Prescricao(models.Model):
    # Protegido: Não se pode apagar uma consulta se houver prescrições para ela.
    consulta = models.ForeignKey(Consulta, on_delete=models.PROTECT, related_name="prescricoes")
    # Protegido: Não se pode apagar um medicamento se ele já foi prescrito.
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    posologia = models.TextField(help_text="Instruções de uso. Ex: 1 comprimido a cada 8 horas por 7 dias.")
    data_prescricao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescrição de {self.medicamento.nome_comercial} para {self.consulta.paciente.nome_completo}"

    class Meta:
        verbose_name = "Prescrição"
        verbose_name_plural = "Prescrições"