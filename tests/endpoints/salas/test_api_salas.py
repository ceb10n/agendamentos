# -*- coding: utf-8 -*-
import json
import pytest
import uuid

from agendamentos.models import db, Sala
from agendamentos.services import AgendaService
from agendamentos import create_app


@pytest.fixture(scope='module')
def agendamentos_app():
    app = create_app(testing=True)
    test_app = app.test_client()

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield test_app

    ctx.pop()


# Testes POST

def test_deve_adicionar_uma_sala(agendamentos_app):
    response = agendamentos_app.post(
        '/v1/salas',
        follow_redirects=True,
        data=json.dumps({
            "codigo": "ADA",
            "nome": "Ada"
        }),
        headers={
            'Content-Type': 'application/json'
        })

    assert response.status_code == 201


def test_deve_retornar_400_para_informacoes_erradas(agendamentos_app):
    response = agendamentos_app.post(
        '/v1/salas',
        follow_redirects=True,
        data=json.dumps({
            "codigo": "ADA"
        }),
        headers={
            'Content-Type': 'application/json'
        })

    assert response.status_code == 400


def test_deve_retornar_415_se_nao_enviar_content_type_ao_criar_sala(agendamentos_app): # noqa
    response = agendamentos_app.post(
        '/v1/salas',
        follow_redirects=True,
        data=json.dumps({
            "codigo": "ADA"
        }))

    assert response.status_code == 415


# Testes GET


def test_deve_retornar_200_ao_listar_salas(agendamentos_app): # noqa
    response = agendamentos_app.get('/v1/salas')

    assert response.status_code == 200


def test_deve_retornar_404_caso_a_sala_nao_exista(agendamentos_app):
    response = agendamentos_app.get('/v1/salas/1')

    assert response.status_code == 404


# Testes PUT


def test_deve_retornar_200_ao_editar_a_sala_com_sucesso(agendamentos_app):
    response = agendamentos_app.post(
        '/v1/salas',
        follow_redirects=True,
        data=json.dumps({
            "codigo": "TESTE_PUT",
            "nome": "Ada put"
        }),
        headers={
            'Content-Type': 'application/json'
        })

    assert response.status_code == 201

    data = json.loads(str(response.get_data(as_text=True)))
    print(data)
    print(data)
    id = data['data']['id']

    response = agendamentos_app.put(
        '/v1/salas/' + id,
        follow_redirects=True,
        data=json.dumps({
            "codigo": "ADA TESTE",
            "nome": "Ada TESTE"
        }),
        headers={
            'Content-Type': 'application/json'
        })

    assert response.status_code == 200
