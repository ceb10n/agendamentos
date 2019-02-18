# -*- coding: utf-8 -*-
from flask import jsonify
from marshmallow.exceptions import ValidationError

from .exceptions import BadRequestError


def get_json(schema, json):
    """Realiza o carregamento do json para o schema.

    Args:
        schema (:obj:`marshmallow.Schema`): A instância do schema que será
            retornado
        json (:obj:`json`): O json que será utilizado pelo schema

    Returns:
        :obj:`marshmallow.Schema`: O schema gerado a partir do json

    Raises:
        :obj:`agendamentos.endpoints.exceptions.BadRequestError`: Caso
            ocorra algum erro de validação de acordo com o schema informado
    """
    try:
        schema = schema.load(json)

        return schema

    except ValidationError as val_err:
        req_err = BadRequestError(status=400)
        req_err.set_errors(val_err.messages)

        raise req_err


def ok(data={}, mensagem="200 OK"):
    """Retorna um response 200 OK."""
    return response(True, data, mensagem, 200)


def created(data={}, mensagem="201 Created"):
    """Retorna um response 201 Created."""
    return response(True, data, mensagem, 201)


def bad_request(data={}, mensagem="400 Bad Request"):
    """Retorna um response 400 Bad Request."""
    return response(False, data, mensagem, 400)


def internal_error(data={}, mensagem="500 Internal Server Error"):
    """Retorna um response 500 Internal Server Error"""
    return response(False, data, mensagem, 500)


def response(sucesso, data, msg, codigo):
    """Retorna um :class:`~flask.Flask.response_class`"""
    return jsonify({
        'success': sucesso,
        'data': data,
        'message': msg
    }), codigo
