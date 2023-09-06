import json
from datetime import datetime
from rest_framework import status
from agenda.models import Agendamento
from rest_framework.test import APITestCase


class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/agendamento_list')
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=datetime(2023, 9, 2),
            nome_cliente="Luana52",
            email_cliente="Luana52@Luana52.com",
            telefone_cliente='123456789012'
        )

        agendamento_serializado = {
            "data_horario": "2023-09-02T00:00:00Z",
            "nome_cliente": "Luana52",
            "email_cliente": "Luana52@Luana52.com",
            "telefone_cliente": '123456789012'
        }

        response = self.client.get(
            path='/api/agendamento_list',
        )
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)
