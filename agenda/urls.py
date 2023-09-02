from django.urls import path
from agenda.views import (
    agendamento_detail,
    agendamento_list,
)

urlpatterns = [
    path('agendamento_list', agendamento_list),
    path('agendamento/<int:id>/', agendamento_detail)
]
