from django.shortcuts import render

# Create your views here.

# core/views.py
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime

# Importando os serviços
from .services import AgendamentoService, ProntuarioService

# A "injeção" acontece aqui, instanciando o serviço para ser usado na view.
# Em projetos maiores, um container de injeção de dependência poderia ser usado.
agendamento_service = AgendamentoService()
prontuario_service = ProntuarioService()

@require_http_methods(["POST"])
def criar_consulta(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        paciente_id = data['paciente_id']
        medico_id = data['medico_id']
        data_hora_str = data['data_hora'] # Formato esperado: "2024-12-25 14:30"
        data_hora = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')

        # A view DELEGA a lógica de negócio para o serviço
        consulta = agendamento_service.agendar_consulta(paciente_id, medico_id, data_hora)
        
        return JsonResponse({'status': 'sucesso', 'consulta_id': consulta.id}, status=201)
    except (ValueError, KeyError) as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

@require_http_methods(["POST"])
def adicionar_registro_prontuario(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        paciente_id = data['paciente_id']
        registro = data['registro']

        # A view DELEGA a lógica de negócio para o serviço
        prontuario = prontuario_service.adicionar_registro(paciente_id, registro)

        return JsonResponse({'status': 'sucesso', 'paciente_id': prontuario.paciente.id}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)

