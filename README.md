<h1>Meu portfólio</h1>
<h3>Objetivo:</h3>
    <p>
        Criar uma API Rest sss
    </p>
    
<h3>Como Funciona:</h3>
    <p>
        Para rodando o projeto localmente, você precisara realizar os seguintes passos:
    </p>
    
   * Crie um ambiente virtual dentro da pasta /Meu-Portfolio `python3 -m venv venv`
   * Acesse a pasta /apps `cd apps/`
   * Execute o comando `pip install -r requirements.txt` para instalar as dependências
   * Execute o comando `python manage.py migrate` para gerar o banco de dados sqlite3
   * Execute o comando `python manage.py createsuperuser` e informe usuário e senha para criar um administrador
   * Acesse a pasta /apps/apps `cd apps/apps` e crie um arquivo .env
   * Dentro arquivo .env defina `DEBUG=True` e configure a SECRET_KEY `SECRET_KEY='COLOQUE_AQUI_SUA_SECRET_KEY'`.
   * Execute o comando `python manage.py runserver` para inicar o projeto
   * Acesse o endereço `localhost:8000` para ver o projeto rodando.
   * Acesse o endereço `localhost:8000/samueloficial@protonmail.com` para fazer as configurações no site.
   

<h3> O que aprendi:</h3>
    <p>
        ...
    </p>

<h3>Tecnologias utilizadas:</h3>

  - Linguagens:
    - python==3.10.4
  
  - Libs:
    - asgiref==3.5.2
    - autopep8==1.7.0
    - dj-database-url==1.0.0
    - Django==4.1
    - django-crispy-forms==1.14.0
    - django-filter==22.1
    - django-on-heroku==1.1.2
    - gunicorn==20.1.0
    - Pillow==9.2.0
    - psycopg2-binary==2.9.3
    - pycodestyle==2.9.1
    - python-decouple==3.6
    - sqlparse==0.4.2
    - toml==0.10.2  
    - whitenoise==6.2.0
    - djangorestframework==3.13.1

  - Framework:
    - Django==4.1
