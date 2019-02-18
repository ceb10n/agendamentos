# -*- coding: utf-8 -*-
import pytest

from marshmallow.exceptions import ValidationError

from agendamentos.endpoints.users import UsuarioSchema


# Testes do UsuarioSchema

def test_usuario_schema_deve_carregar_corretamente():
    usuario_schema = UsuarioSchema()
    usuario = usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'teste@gmail.com',
            'senha': 'senha_muito_dificil'
        })

    assert usuario['nome'] == 'Rafael Marques'
    assert usuario['email'] == 'teste@gmail.com'
    assert usuario['senha'] == 'senha_muito_dificil'


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


def test_usuario_schema_email_nao_deve_ter_menos_de_7_caracteres():
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


# Validações da senha

def test_usuario_schema_senha_deve_ser_obrigatorio():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'email@gmail.com'
        })

    val_err = excinfo.value
    assert val_err.messages['senha'][0] == 'A senha é obrigatória'


def test_usuario_schema_senha_deve_nao_deve_ser_nula():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'email@gmail.com',
            'senha': None
        })

    val_err = excinfo.value
    assert val_err.messages['senha'][0] == 'A senha não pode ser nula'


def test_usuario_schema_senha_deve_nao_deve_ter_menos_de_6_caracteres():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'email@gmail.com',
            'senha': 'senha'
        })

    val_err = excinfo.value
    assert val_err.messages['senha'][0] == 'A senha deve conter entre 6 e 50 caracteres' # noqa


def test_usuario_schema_senha_deve_nao_deve_ter_mais_de_50_caracteres():
    usuario_schema = UsuarioSchema()

    with pytest.raises(ValidationError) as excinfo:
        usuario_schema.load({
            'nome': 'Rafael Marques',
            'email': 'email@gmail.com',
            'senha': 's' * 51
        })

    val_err = excinfo.value
    assert val_err.messages['senha'][0] == 'A senha deve conter entre 6 e 50 caracteres' # noqa
