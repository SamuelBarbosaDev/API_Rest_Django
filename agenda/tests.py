import json
from rest_framework.test import APITestCase
from rest_framework import status


class TestListagemAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/agendamento_list')
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        data = {
            "data_horario": "2023-09-02T05:08:10Z",
            "nome_cliente": "Luana52",
            "email_cliente": "Luana52@Luana52.com",
            "telefone_cliente": 123456789012
        }

        response = self.client.post(
            path='/api/agendamento_list',
            data=data,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
