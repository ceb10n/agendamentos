# Gestão de Salas de Reuniões

## Requisitos

* Disponibilizar o projeto em algum repositório
* O Webservice deve seguir os princípios REST
* Salvar as informações necessárias em um banco de dados (relacional ou não), de sua escolha
* Testes automatizados com informação da cobertura de testes
* Gerar logs das ações
* Documentar como rodar o projeto

## Entregáveis

### sistema de agendamento precisa ter:


 * Uma API para criar, editar e remover agendamentos
 * Uma API para listar e filtrar agendamentos por data e sala
 * Uma API para criar, editar e remover salas de reuniões

### Gestão das salas de reuniões do nosso escritório.

Esse sistema deve receber requisições de agendamento contendo título, sala e período de agendamento e deve apenas reservar a sala, se a sala requisitada estiver disponível. Caso contrário, deve apresentar um erro.

# Instalando o Projeto

O projeto foi desenvolvido em Python 3 e Flask, tornando o python uma dependência obrigatória para o projeto.

Para maiores informações sobre como instalar o python em sua máquina, visitar:

* [https://python.org](https://www.python.org/)


## Obtendo o Projeto e preparando o ambiente

```console
git clone https://github.com/ceb10n/agendamentos.git
cd agendamentos
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt 
```

*O virtualenv é opcional, mas desejável*

*O docker machine também é opcional, mas pode ser utilizado para levantar o banco de dados da aplicação*

## Banco de Dados

O projeto utiliza uma instância do Postgres que é levantada com o docker (ver o arquivo docker-compose.yml).
Para os testes, é utilizado o sqlite em memória.

Para rodar o projeto, será necessário ou criar uma docker machine localmente e rodar o comando:

`docker-compose up -d --build`

Para levantar o banco de dados com as informações contidas na variável de ambiente `SQLALCHEMY_DATABASE_URI` descrita no tópico de variáveis de ambiente.

É possível também utilizar qualquer outro postgres, porém será necessário atualizar as informações da connection string.

Observação:

É possível rodar o projeto sem o Postgres, utilizando diramente o sqlite em memória.
Basta definir a variável de ambiente:

`SQLALCHEMY_DATABASE_URI="sqlite://"`

Porém, o filtro de agendamentos por data não está compatível com o SQLite, impossibilitando realizar tal query.

## Rodando o projeto

A maneira mais simples de iniciar o projeto é rodando o seguinte comando a partir da pasta raíz do projeto:

```console
python3 agendamentos/app.py
```

## Variáveis de ambiente

O projeto `agendamentos` depende de algumas variáveis de ambientes para rodar perfeitamente.

```
APP_PORTA=5000
AMBIENTE="development"
SENTRY_DNS=""
SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://agendamentos:agendamentos@192.168.99.100:5432/agendamentos"
SQLALCHEMY_TRACK_MODIFICATIONS="False"
```

Para obter o dns do Sentry, basta criar uma conta gratuitamente em [https://sentry.io](https://sentry.io) e adicioná-la na variável de ambiente `SENTRY_DNS`

É possível também adicionar as variáveis de ambiente em um arquivo `.env` dentro da pasta `agendamentos/agendamentos`, que ao iniciar o projeto, o pacote `dotenv` inicializará todas as variáveis do arquivo.

O endereço do banco de dados é relativo ao Postgres que é criado com o docker-compose.yml. Para utilizar algum outro banco, com endeço diferente, etc. Basta atualizar as informações da string de conexão.
É importante lembrar que o ip da sua docker machine pode ser diferente.

## Informações sobre os endpoints

Está disponível através da url `/apidocs` a documentação dos endpoints.

É utilizado o pacote `flasgger` para gerar toda a documentação com o Swagger.

![swagger agendamentos](imgs/swagger.png)

## Testando o projeto

```console
pip install -e .
pytest --cov=agendamentos tests/
coverage html
```

Basta ir para a pasta `htmlcov` na raíz do projeto que estará disponível em html o relatório de cobertura de testes do projeto.


### Rastreamento de erros

A aplicação está utilizando o [Sentry](https://sentry.io).

![sentry.io](imgs/sentry.png)

Para utilizar a integração, é necessário configurar a variável de ambiente `SENTRY_DNS` com o valor do dns disponibilizado pelo Sentry.
