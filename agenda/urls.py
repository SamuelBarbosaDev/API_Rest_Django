from django.urls import path
from agenda.views import (
    AgendamentoDetail,
    AgendamentoList,
    prestador_list,
    get_horarios,
    healthcheck,
)

urlpatterns = [
    path('agendamento_list/', AgendamentoList.as_view()),
    path('agendamento/<int:pk>/', AgendamentoDetail.as_view()),
    path('prestador_list/', prestador_list),
    path('get_horarios/', get_horarios),
    path('', healthcheck),
]
