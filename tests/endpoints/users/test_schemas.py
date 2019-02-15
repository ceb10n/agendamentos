# -*- coding: utf-8 -*-
import pytest

from marshmallow.exceptions import ValidationError

from agendamentos.endpoints.users import UsuarioSchema


# Testes do UsuarioSchema

# Validações do nome

def test_usuario_schema_nome_deve_ser_obrigatorio():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'email': 'teste@gmail.com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome é obrigatório'


def test_usuario_schema_nome_nao_deve_ser_nulo():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': None,
            'email': 'teste@gmail.com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome não pode ser nulo'


def test_usuario_schema_nome_nao_deve_ter_menos_de_2_caracteres():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'a',
            'email': 'teste@gmail.com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome deve conter entre 2 e 100 caracteres' # noqa


def test_usuario_schema_nome_nao_deve_ter_mais_de_100_caracteres():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'a' * 101,
            'email': 'teste@gmail.com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['nome'][0] == 'O nome deve conter entre 2 e 100 caracteres' # noqa


# Validações do E-mail


def test_usuario_schema_email_deve_ser_obrigatorio():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['email'][0] == 'O e-mail é obrigatório'


def test_usuario_schema_email_nao_deve_ser_nulo():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': None,
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['email'][0] == 'O e-mail não pode ser nulo'


def test_usuario_schema_email_nao_deve_ter_menos_de_6_caracteres():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'a@a.cc',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['email'][0] == 'O e-mail deve conter entre 7 e 100 caracteres' # noqa


def test_usuario_schema_email_nao_deve_ter_mais_de_100_caracteres():
    usuario_schema = UsuarioSchema()
    email = 'a' * 99

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': f'{email}@globo.com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['email'][0] == 'O e-mail deve conter entre 7 e 100 caracteres' # noqa


def test_usuario_schema_email_deve_ser_valido():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'email_invalido_ponto_com',
            'senha': 'senha_muito_dificil'
        })

    val_err = excinfo.value
    assert val_err.messages['email'][0] == 'O e-mail informado não é válido'
