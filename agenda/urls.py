from django.urls import path
from agenda.views import (
    AgendamentoDetail,
    AgendamentoList,
    PrestadorList,
    get_horarios
)

urlpatterns = [
    path('agendamento_list/', AgendamentoList.as_view()),
    path('agendamento/<int:pk>/', AgendamentoDetail.as_view()),
    path('prestador_list/', PrestadorList.as_view()),
    path('get_horarios/', get_horarios),
]
