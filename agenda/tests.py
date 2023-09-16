import json
from unittest import mock
from rest_framework import status
from agenda.models import Agendamento
from datetime import datetime, timezone
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class TestListagemAgendamentos(APITestCase):
    def setUp(self):
        # Crie um usuário para autenticação
        self.user = User.objects.create_user(
            username='user',
            password='1234'
        )
        # Autentique o usuário
        self.client.login(
            username='user',
            password='1234'
        )
        # Serializando agendamento
        self.agendamento_serializado = {
            'id': 1,
            'prestador': 'user',
            'data_horario': '2024-09-02T00:00:00Z',
            'nome_cliente': 'user',
            'email_cliente': 'user@user.com',
            'telefone_cliente': '012345678912',
        }

    def test_listagem_vazia(self):
        # Faça a solicitação GET autenticada
        response = self.client.get('/api/agendamento_list/?username=user')
        data = json.loads(response.content)
        print(data)

        # Verifique se a resposta está vazia
        self.assertEqual(data, [])

    def test_listagem_de_agendamentos_criados(self):
        # Crie um agendamento
        Agendamento.objects.create(
            prestador=self.user,
            data_horario=datetime(
                2024, 9, 2,
                tzinfo=timezone.utc
            ),
            nome_cliente='user',
            email_cliente='user@user.com',
            telefone_cliente='012345678912',
        )

        # Faça a solicitação GET
        response = self.client.get(
            path='/api/agendamento_list/?username=user',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifique se o agendamento criado está na lista
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        self.assertDictEqual(data[0], self.agendamento_serializado)


class TestCriacaoAgendamento(APITestCase):
    def setUp(self):
        # Crie um usuário para autenticação
        self.user = User.objects.create_user(
            username='user',
            password='1234',
        )
        # Autentique o usuário
        self.client.login(
            username='user',
            password='1234',
        )
        # Serializando agendamento
        self.agendamento_serializado = {
            "id": 1,
            "data_horario": "2024-09-12T09:00:00Z",
            "nome_cliente": "user",
            "email_cliente": "user@user.com",
            "telefone_cliente": "012345678912",
            "prestador": "user"
        }

    def test_cria_agendamento(self):
        # Fazendo uma requisição POST
        response = self.client.post(
            path='/api/agendamento_list/?username=user',
            data=self.agendamento_serializado,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Verifique o harário do agendamento
        agendamento_criado = Agendamento.objects.get()
        agendamento_criado.data_horario = datetime(
            2024, 9, 2,
            tzinfo=timezone.utc
        )
        self.assertEqual(
            agendamento_criado.data_horario,
            datetime(
                2024, 9, 2,
                tzinfo=timezone.utc
            )
        )

    def test_verificando_se_a_api_retorna_objeto_criado(self):
        # Fazendo uma requisição POST
        response_post = self.client.post(
            path='/api/agendamento_list/?username=user',
            data=self.agendamento_serializado,
            format='json'
        )
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        # Fazendo uma requisição GET
        response_get = self.client.get(
            path='/api/agendamento_list/?username=user',
        )
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Comparando a resposta GET com o agendamento serializado
        data = json.loads(response_get.content)
        self.assertEqual(
            data[0],
            self.agendamento_serializado
        )

    def test_quando_request_e_invalido_retorna_400(self):
        agendamento_serializado = {
            "id": 1,
            "prestador": "user",
            "data_horario": "erro",
            "nome_cliente": "user",
            "email_cliente": "user@user.com",
            "telefone_cliente": "012345678912",
        }
        response = self.client.post(
            path='/api/agendamento_list/?username=user',
            data=agendamento_serializado,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestGetHorarios(APITestCase):
    @mock.patch('agenda.libs.brasil_api.is_feriado', return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        # Fazendo requisição GET
        response = self.client.get(path='/api/get_horarios/?data=2024-12-25')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificando se o retorno é uma lista vazia
        data = json.loads(response.content)
        self.assertEqual(data, [])

    @mock.patch('agenda.libs.brasil_api.is_feriado', return_value=False)
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self, _):
        # Fazendo requisição GET
        response = self.client.get(path='/api/get_horarios/?data=2024-09-15')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificando se o retorno é uma lista Não vazia
        data = json.loads(response.content)
        self.assertNotEqual(data, [])

        # Verificando se o retorno é uma lista Não vazia
        self.assertEqual(data[2], '2024-09-15T10:00:00Z')
