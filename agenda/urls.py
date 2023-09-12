from django.urls import path
from agenda.views import (
    AgendamentoDetail,
    AgendamentoList
)

urlpatterns = [
    path('agendamento_list/', AgendamentoList.as_view()),
    path('agendamento/<int:pk>/', AgendamentoDetail.as_view())
]
