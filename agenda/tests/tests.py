import json
from unittest import mock
from decouple import config
from django.core import mail
from rest_framework import status
from agenda.models import Agendamento
from datetime import datetime, timezone
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from agenda.tasks import gera_relatorio, envia_email


TEST_USER = config('TEST_USER', default='user')
TEST_PASSAWORD = config('TEST_PASSAWORD', default='******')


class TestListagemAgendamentos(APITestCase):
    def setUp(self):
        # Crie um usuário para autenticação
        self.user = User.objects.create_user(
            username=TEST_USER,
            password=TEST_PASSAWORD
        )
        # Autentique o usuário
        self.client.login(
            username=TEST_USER,
            password=TEST_PASSAWORD
        )
        # Serializando agendamento
        self.agendamento_serializado = {
            'id': 1,
            'prestador': TEST_USER,
            'data_horario': '2024-09-02T00:00:00Z',
            'nome_cliente': 'user',
            'email_cliente': 'user@user.com',
            'telefone_cliente': '012345678912',
        }

    def test_listagem_vazia(self):
        # Faça a solicitação GET autenticada
        response = self.client.get(
            f'/api/agendamento_list/?username={TEST_USER}'
        )
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
            path=f'/api/agendamento_list/?username={TEST_USER}',
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
            username=TEST_USER,
            password=TEST_PASSAWORD,
        )
        # Autentique o usuário
        self.client.login(
            username=TEST_USER,
            password=TEST_PASSAWORD,
        )
        # Serializando agendamento
        self.agendamento_serializado = {
            "id": 1,
            "data_horario": "2024-09-12T09:00:00Z",
            "nome_cliente": "user",
            "email_cliente": "user@user.com",
            "telefone_cliente": "012345678912",
            "prestador": TEST_USER
        }

    def test_cria_agendamento(self):
        # Fazendo uma requisição POST
        response = self.client.post(
            path=f'/api/agendamento_list/?username={TEST_USER}',
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
            path=f'/api/agendamento_list/?username={TEST_USER}',
            data=self.agendamento_serializado,
            format='json'
        )
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        # Fazendo uma requisição GET
        response_get = self.client.get(
            path=f'/api/agendamento_list/?username={TEST_USER}',
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


class TestGetEmail(APITestCase):
    def setUp(self):
        # Crie um usuário para autenticação
        self.user = User.objects.create_superuser(
            username=TEST_USER,
            email='user@test.com',
            password=TEST_PASSAWORD
        )
        # Autentique o usuário
        self.client.login(
            username=TEST_USER,
            password=TEST_PASSAWORD
        )

    def test_envio_tarefas(self):
        # Requisição GET:
        response = self.client.get('/api/prestador_list/?formato=csv')
        assert response.status_code, status.HTTP_200_OK

        # Verificando task
        data = json.loads(response.content)
        assert data['task_id'], str

    def test_envio_email(self):
        envia_email(self.user.email)
        assert len(mail.outbox), 1

    def test_gera_relatorio(self):
        # Verificando o tipo da saída
        retorna = gera_relatorio()
        self.assertEqual(type(retorna), str)

        # Verificando se é um csv
        csv = 'datetime,name,email,phone_number,prestador\r\n'
        self.assertEqual(retorna, csv)
