# API Rest Django

### Índice:

- [API Rest Django](#api-rest-django)
    - [Índice:](#índice)
  - [Contextualizando](#contextualizando)
  - [Rotas da API](#rotas-da-api)
    - [Listar os horários disponíveis:](#listar-os-horários-disponíveis)
    - [Listar os agendamentos do usuário:](#listar-os-agendamentos-do-usuário)
    - [Lista todos os agendamentos de todos os prestadores:](#lista-todos-os-agendamentos-de-todos-os-prestadores)
    - [Gera um CSV com os agendamentos de todos os prestadores:](#gera-um-csv-com-os-agendamentos-de-todos-os-prestadores)
    - [Cria um novo agendamento:](#cria-um-novo-agendamento)
    - [Lista um agendamento:](#lista-um-agendamento)
    - [Faz uma alteração parcial de um agendamento:](#faz-uma-alteração-parcial-de-um-agendamento)
    - [Faz uma alteração total:](#faz-uma-alteração-total)
    - [Deleta um agendamento:](#deleta-um-agendamento)
  - [Implantação:](#implantação)
  - [Pré-requisitos para executar o projeto:](#pré-requisitos-para-executar-o-projeto)
    - [Ambiente virtual e Dependências:](#ambiente-virtual-e-dependências)

## Contextualizando
Este é um repositório que contém uma API Rest desenvolvida em Django, projetada para criar e gerenciar agendamentos. A API oferece uma variedade de rotas para lidar com diferentes aspectos de agendamentos. Abaixo estão as principais rotas e suas descrições:

## Rotas da API
A seguir estão listadas as rotas da API com os métodos HTTP correspondentes e os parâmetros necessários, quando aplicável.

### Listar os horários disponíveis:
- **Método**: GET
- **Rota**: 
```url
  /api/get_horarios/?data=2023-01-02
```
- **Descrição**: Retorna os horários disponíveis para a data especificada.

### Listar os agendamentos do usuário:

- **Método**: GET
- **Rota**: 
```url
  /api/agendamento_list/?username=name
```
- **Descrição**: Retorna a lista de agendamentos do usuário com o nome de usuário especificado.

### Lista todos os agendamentos de todos os prestadores:

- **Método**: GET
- **Rota**: 
```url
  /api/prestador_list/
```
- **Descrição**: Retorna a lista de todos os agendamentos de todos os prestadores.

### Gera um CSV com os agendamentos de todos os prestadores:

- **Método**: GET
- **Rota**: 
```url
  /api/prestador_list/?formato=csv
```
- **Descrição**: Gera um arquivo CSV contendo os agendamentos de todos os prestadores.

### Cria um novo agendamento:

- **Método**: POST
- **Rota**: 
```url
  /api/agendamento_list/?username=name
```
- **Descrição**: Cria um novo agendamento para o usuário com o nome de usuário especificado.

### Lista um agendamento:

- **Método**: GET
- **Rota**: 
```url
  /api/agendamento/pk/?username=name
```
- **Descrição**: Retorna os detalhes de um agendamento específico com base no ID (pk) especificado.

### Faz uma alteração parcial de um agendamento:

- **Método**: PATCH
- **Rota**: 
```url
  /api/agendamento/pk/?username=name
```
- **Descrição**: Realiza uma alteração parcial em um agendamento específico com base no ID (pk) especificado para o usuário com o nome de usuário especificado.

### Faz uma alteração total:

- **Método**: PUT
- **Rota**: 
```url
  /api/agendamento/pk/?username=name
```
- **Descrição**: Realiza uma alteração total em um agendamento específico com base no ID (pk) especificado para o usuário com o nome de usuário especificado.

### Deleta um agendamento:

- **Método**: DELETE
- **Rota**: 
```url
  /api/agendamento/pk/?username=name
```
- **Descrição**: Deleta um agendamento específico com base no ID (pk) especificado para o usuário com o nome de usuário especificado.

  
## Implantação:
Iniciando a etapa de implementação do projeto em produção.

## Pré-requisitos para executar o projeto:
Abaixo, listarei os requisitos necessários para que o projeto funcione corretamente.

### Ambiente virtual e Dependências:
Criando ambiente virtual:
```
python3.10 -m venv core/.venv
```

Entrando no ambiente virtual:
```
source .venv/bin/activate
```

Instale as dependências:
```
pip install -r requirements.txt
```
---
Linkedin: <https://www.linkedin.com/in/name-barbosa-dev/> 

E-mail: <nameoficial@protonmail.com>
