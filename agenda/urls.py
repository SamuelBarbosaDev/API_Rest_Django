from django.urls import path
from agenda.views import (
    agendamento_detail
)

urlpatterns = [
    path('agendamento/<int:id>/', agendamento_detail)
]
