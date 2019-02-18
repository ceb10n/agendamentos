# -*- coding: utf-8 -*-
import pytest

from marshmallow.exceptions import ValidationError

from agendamentos.endpoints.salas import SalaSchema


# Testes do SalaSchema

def test_sala_schema_deve_carregar_corretamente():
    sala_schema = SalaSchema()
    sala = sala_schema.load({
            'nome': 'Sala do Conhecimento',
            'codigo': 'SALA_CON'
        })

    assert sala['nome'] == 'Sala do Conhecimento'
    assert sala['codigo'] == 'SALA_CON'


# Validações do nome

def test_sala_schema_nome_deve_ser_obrigatorio():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'codigo': 'SALA_CON'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome é obrigatório'


def test_sala_schema_nome_nao_deve_ser_nulo():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': None,
            'codigo': 'SALA_CON'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome não pode ser nulo'


def test_sala_schema_nome_nao_deve_ter_menos_de_2_caracteres():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'a',
            'codigo': 'SALA_CON'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome deve conter entre 2 e 100 caracteres' # noqa


def test_sala_schema_nome_nao_deve_ter_mais_de_100_caracteres():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'a' * 101,
            'codigo': 'SALA_CON'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome deve conter entre 2 e 100 caracteres' # noqa


# Validações do código

def test_sala_schema_codigo_deve_ser_obrigatorio():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'Sala Auto Conhecimento'
        })

    val_err = excinfo.value
    assert val_err.messages['codigo'][0] == 'O código é obrigatório'


def test_sala_schema_codigo_nao_deve_ser_nulo():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'Sala Auto Conhecimento',
            'codigo': None
        })

    val_err = excinfo.value
    assert val_err.messages['codigo'][0] == 'O código não pode ser nulo'


def test_sala_schema_codigo_nao_deve_ter_menos_de_2_caracteres():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'Sala Auto Conhecimento',
            'codigo': 'S'
        })

    val_err = excinfo.value
    assert val_err.messages['codigo'][0] == 'O código deve conter entre 2 e 15 caracteres' # noqa


def test_sala_schema_codigo_nao_deve_ter_mais_de_15_caracteres():
    sala_schema = SalaSchema()

    with pytest.raises(ValidationError) as excinfo:
        sala_schema.load({
            'nome': 'Sala Auto Conhecimento',
            'codigo': 'S' * 16
        })

    val_err = excinfo.value
    assert val_err.messages['codigo'][0] == 'O código deve conter entre 2 e 15 caracteres' # noqa
