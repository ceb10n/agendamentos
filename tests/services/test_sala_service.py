# -*- coding: utf-8 -*-
import pytest
import uuid

from agendamentos.models import db
from agendamentos.services import SalaService
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


def test_adicionar_uma_sala_com_sucesso(agendamentos_app):
    service = SalaService()

    sala = service.adicionar(
        nome='Sala de Teste',
        codigo='SALA_TESTE')

    assert sala.nome == 'Sala de Teste'
    assert sala.codigo == 'SALA_TESTE'


def test_listar_salas(agendamentos_app):
    service = SalaService()
    id = str(uuid.uuid4())
    service.adicionar(id=id, nome='Sala de Teste', codigo='SALA_TESTE')

    salas = service.listar()

    assert len(salas) > 0


def test_procurar_sala_por_id(agendamentos_app):
    service = SalaService()
    sala = service.adicionar(nome='Sala de Teste', codigo='SALA_TESTE')

    sala = service.procurar_por_id(sala.id)

    assert sala.nome == 'Sala de Teste'
    assert sala.codigo == 'SALA_TESTE'


def test_editar_sala(agendamentos_app):
    service = SalaService()
    sala = service.adicionar(nome='Sala de Teste', codigo='SALA_TESTE')

    assert service.editar(sala.id, {
        'nome': 'Nome Editado',
        'codigo': 'Código Editado'}) is True

    sala = service.procurar_por_id(sala.id)

    assert sala.nome == 'Nome Editado'
    assert sala.codigo == 'Código Editado'


def test_editar_sala_deve_retornar_false_se_a_sala_nao_existir(agendamentos_app): # noqa
    service = SalaService()
    id = str(uuid.uuid4())

    assert not service.editar(id, {
        'nome': 'Nome Editado',
        'codigo': 'Código Editado'})


def test_remover_uma_sala_com_sucesso(agendamentos_app):
    service = SalaService()

    sala = service.adicionar(
        nome='Sala de Teste',
        codigo='SALA_TESTE')

    assert service.remover(sala.id) is True


def test_remover_uma_sala_que_nao_existe_deve_retornar_falso(agendamentos_app):
    service = SalaService()
    id = str(uuid.uuid4())

    assert not service.remover(id)
