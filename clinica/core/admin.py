from django.contrib import admin

# Register your models here.

# core/admin.py
from django.contrib import admin
from .models import (
    Especialidade, Medico, Convenio, Paciente, Consulta, 
    Prontuario, Exame, PedidoExame, Medicamento, Prescricao
)

admin.site.register(Especialidade)
admin.site.register(Medico)
admin.site.register(Convenio)
admin.site.register(Paciente)
admin.site.register(Consulta)
admin.site.register(Prontuario)
admin.site.register(Exame)
admin.site.register(PedidoExame)
admin.site.register(Medicamento)
admin.site.register(Prescricao)