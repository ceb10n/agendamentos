# -*- coding: utf-8 -*-
from flask import jsonify, make_response
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


def created(data={}, mensagem="201 Created", location=''):
    """Retorna um response 201 Created."""
    headers = {'Location': location}
    return response(True, data, mensagem, 201, headers=headers)


def bad_request(data={}, mensagem="400 Bad Request"):
    """Retorna um response 400 Bad Request."""
    return response(False, data, mensagem, 400)


def not_found(mensagem="404 Not Found"):
    """Retorna um response 404 Not Found."""
    return response(False, {}, mensagem, 404)


def internal_error(data={}, mensagem="500 Internal Server Error"):
    """Retorna um response 500 Internal Server Error"""
    return response(False, data, mensagem, 500)


def unsuported_media_type(data={}, mensagem="415 Unsupported Media Type"):
    """Retorna um response 415 Unsupported Media Type"""
    return response(False, data, mensagem, 415)


def response(sucesso, data, msg, codigo, headers=None):
    """Retorna um :class:`~flask.Flask.response_class`"""
    retorno = jsonify({
        'success': sucesso,
        'data': data,
        'message': msg})

    if headers:
        response = make_response(retorno, codigo)
        for k, v in headers.items():
            response.headers[k] = v

        return response

    return retorno, codigo
