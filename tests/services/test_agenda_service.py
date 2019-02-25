# -*- coding: utf-8 -*-
import datetime
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

    sala1 = Sala(id=str(uuid.uuid4()), nome='Sala de Teste 1', codigo='TEST_SALA_1') # noqa
    db.session.add(sala1)

    sala2 = Sala(id=str(uuid.uuid4()), nome='Sala de Teste 2', codigo='TEST_SALA_2') # noqa
    db.session.add(sala2)

    sala3 = Sala(id=str(uuid.uuid4()), nome='Sala de Teste 3', codigo='TEST_SALA_3') # noqa
    db.session.add(sala3)

    sala4 = Sala(id=str(uuid.uuid4()), nome='Sala de Teste 4', codigo='TEST_SALA_4') # noqa
    db.session.add(sala4)

    db.session.commit()

    yield test_app

    ctx.pop()


def test_adicionar_um_agendamento_com_sucesso(agendamentos_app):
    service = AgendaService()
    sala = Sala.query.first()
    agora = datetime.datetime.utcnow()

    agenda = service.adicionar(
        inicio=agora,
        fim=agora,
        sala_id=sala.id)

    assert agenda.id is not None
    assert agenda.inicio == agora
    assert agenda.fim == agora
    assert agenda.sala_id == sala.id


def test_nao_deve_permitir_agendamento_na_mesma_sala_no_mesmo_horario(agendamentos_app): # noqa
    service = AgendaService()
    sala = Sala.query.first()
    agora = datetime.datetime.utcnow()

    service.adicionar(
        inicio=agora,
        fim=agora,
        sala_id=sala.id)

    with pytest.raises(Exception) as excinfo:
        service.adicionar(
            inicio=agora,
            fim=agora,
            sala_id=sala.id)

    val_err = excinfo.value
    assert str(val_err) == 'A sala já está reservada neste horário'


def test_a_sala_deve_existir(agendamentos_app):
    service = AgendaService()
    agora = datetime.datetime.utcnow()

    with pytest.raises(Exception) as excinfo:
        service.adicionar(
            inicio=agora,
            fim=agora,
            sala_id=str(uuid.uuid4()))

    val_err = excinfo.value
    assert str(val_err) == 'A sala deve ser válida'


def test_deve_achar_o_agendamento_pelo_id(agendamentos_app):
    service = AgendaService()
    sala = Sala.query.first()
    agora = datetime.datetime.utcnow()

    agenda_salva = service.adicionar(
        inicio=agora,
        fim=agora,
        sala_id=sala.id)

    agenda = service.procurar_por_id(agenda_salva.id)

    assert agenda.id == agenda_salva.id


def test_deve_editar_o_agendamento(agendamentos_app):
    service = AgendaService()
    sala = Sala.query.first()
    agora = datetime.datetime.utcnow()

    agenda = service.adicionar(
        inicio=agora,
        fim=agora,
        sala_id=sala.id)

    assert agenda.id is not None
    assert agenda.inicio == agora
    assert agenda.fim == agora
    assert agenda.sala_id == sala.id

    amanha = agora + datetime.timedelta(days=1)
    nova_sala = Sala.query.filter(Sala.codigo == 'TEST_SALA_3').first()

    assert service.editar(agenda.id, {
        'inicio': amanha,
        'fim': amanha,
        'sala_id': nova_sala.id}) is True


def test_editar_deve_retornar_false_para_agenda_nao_existente(agendamentos_app):
    service = AgendaService()

    assert not service.editar(str(uuid.uuid4()), {})


def test_a_sala_deve_ser_obrigatoria(agendamentos_app):
    service = AgendaService()
    agora = datetime.datetime.utcnow()

    with pytest.raises(Exception) as excinfo:
        service.adicionar(inicio=agora, fim=agora)

    val_err = excinfo.value
    assert str(val_err) == 'O id da sala é obrigatório'


def test_deve_remover_a_sala_com_sucesso(agendamentos_app):
    service = AgendaService()
    sala = Sala.query.first()
    agora = datetime.datetime.utcnow()

    agenda = service.adicionar(
        inicio=agora,
        fim=agora,
        sala_id=sala.id)

    assert service.remover(agenda.id) is True


def test_remover_sala_inexistente_deve_retornar_false(agendamentos_app):
    service = AgendaService()

    assert not service.remover(str(uuid.uuid4()))
