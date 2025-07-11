# core/services.py
from datetime import datetime
from .models import Consulta, Prontuario, Paciente, Medico

# Injeção de Dependência 1: Serviço de Agendamento
class AgendamentoService:
    """
    Serviço responsável pela lógica de negócio de agendamento de consultas.
    """
    def agendar_consulta(self, paciente_id: int, medico_id: int, data_hora: datetime) -> Consulta:
        try:
            paciente = Paciente.objects.get(id=paciente_id)
            medico = Medico.objects.get(id=medico_id)

            # Lógica de negócio: Verificar se o médico tem disponibilidade (exemplo simples)
            if Consulta.objects.filter(medico=medico, data_hora=data_hora).exists():
                raise ValueError("Médico indisponível neste horário.")

            consulta = Consulta.objects.create(
                paciente=paciente,
                medico=medico,
                data_hora=data_hora,
                status='AGENDADA'
            )
            return consulta
        except (Paciente.DoesNotExist, Medico.DoesNotExist) as e:
            raise ValueError(f"Erro ao encontrar paciente ou médico: {e}")

# Injeção de Dependência 2: Serviço de Prontuário
class ProntuarioService:
    """
    Serviço para gerenciar a lógica de negócio dos prontuários dos pacientes.
    """
    def adicionar_registro(self, paciente_id: int, novo_registro: str) -> Prontuario:
        paciente = Paciente.objects.get(id=paciente_id)
        prontuario, created = Prontuario.objects.get_or_create(paciente=paciente)
        
        prontuario.historico_medico += f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M')}] {novo_registro}"
        prontuario.save()
        return prontuario