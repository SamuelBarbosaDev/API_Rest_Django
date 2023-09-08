import json
from datetime import datetime, timezone
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
            data_horario=datetime(
                2023, 9, 2,
                tzinfo=timezone.utc
            ),
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


class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_serializado = {
            "data_horario": "2023-03-15T00:00:00Z",
            "nome_cliente": "Luana52",
            "email_cliente": "Luana52@Luana52.com",
            "telefone_cliente": '123456789012'
        }
        # response:
        self.client.post(
            path='/api/agendamento_list',
            data=agendamento_serializado,
            format='json'
        )
        # ---
        agendamento_criado = Agendamento.objects.get()
        agendamento_criado.data_horario = datetime(
            2022, 3, 15,
            tzinfo=timezone.utc
        )
        self.assertEqual(
            agendamento_criado.data_horario,
            datetime(
                2022, 3, 15,
                tzinfo=timezone.utc
            )
        )

    def test_verificando_se_a_api_retorna_objeto_criado(self):
        agendamento_serializado = {
            "data_horario": "2023-03-15T00:00:00Z",
            "nome_cliente": "Usuario",
            "email_cliente": "Usuario@Usuario.com",
            "telefone_cliente": '123456789012'
        }
        # response POST:
        self.client.post(
            path='/api/agendamento_list',
            data=agendamento_serializado,
            format='json'
        )
        # ---
        response = self.client.get(
            path='/api/agendamento_list',
        )
        data = json.loads(response.content)

        self.assertEqual(
            data[0],
            agendamento_serializado
        )

    def test_quando_request_e_invalido_retorna_400(self):
        agendamento_serializado = {
            "data_horario": "202:00Z",
            "nome_cliente": "Luana52",
            "email_cliente": "Luana52@Luana52.com",
            "telefone_cliente": '123456789012'
        }
        response = self.client.post(
            path='/api/agendamento_list',
            data=agendamento_serializado,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
