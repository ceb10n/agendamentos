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

Esse sistema deve receber requisições de agendamento contendo título, sala e período de agendamento e
deve apenas reservar a sala, se a sala requisitada estiver disponível. Caso contrário, deve apresentar um
erro.

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

