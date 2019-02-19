# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from .schemas import EditarSalaSchema, SalaSchema
from ..commons import (
    get_json,
    created,
    internal_error,
    not_found,
    ok,
    unsuported_media_type)
from ..exceptions import BadRequestError
from ...services import SalaService


api_salas_v1 = Blueprint('api_salas_v1', __name__, url_prefix='/v1')


@api_salas_v1.route('/salas', methods=['GET'])
def listar_salas():
    """Retorna todas as salas de reunião.
    ---
    tags:
      - salas
    definitions:
      Sala:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
          id:
            type:
              string
    responses:
      200:
        description: A sala foi criada
        schema:
          type: array
          items:
            $ref: '#/definitions/Sala'
      500:
        description: Um erro não previsto ocorreu
    """
    service = SalaService()

    try:
        salas = service.listar()

        return ok(data=[sala.to_dict() for sala in salas])

    except Exception:
        return internal_error()


@api_salas_v1.route('/salas/<id>', methods=['GET'])
def pesquisar_sala(id):
    """Retorna uma sala de acordo com o seu id.
    ---
    tags:
      - salas
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Id da Sala de Reunião
    definitions:
      Sala:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
    definitions:
      Sala:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
          id:
            type:
              string
    responses:
      200:
        description: A sala foi criada
        schema:
          "$ref": "#/definitions/Sala"
      404:
        description: A Sala de reunião informada não foi encontrada
      500:
        description: Um erro não previsto ocorreu
    """
    service = SalaService()

    try:
        sala = service.procurar_por_id(id)

        if sala:
            return ok(data=sala.to_dict())

        return not_found('Sala não encontrada')

    except Exception:
        return internal_error()


@api_salas_v1.route('/salas', methods=['POST'])
def criar_sala():
    """Cria uma nova sala de reunião.
    ---
    tags:
      - salas
    parameters:
      - name: sala
        in: body
        type: object
        required: true
        "schema": {
          "$ref": "#/definitions/SalaSchema"
        }
    definitions:
      SalaSchema:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
    responses:
      201:
        description: A sala foi criada
      400:
        description: 400 Bad Request
      415:
        description: Media Type não suportado
      500:
        description: Um erro não previsto ocorreu
    """
    if not request.is_json:
        return unsuported_media_type()

    try:
        schema = get_json(SalaSchema(), request.get_json())

    except BadRequestError as bad_req_err:
        return jsonify({
          'errors': bad_req_err.errors,
          'status': bad_req_err.code,
          'mensagem': 'Não foi possível salvar a sala'
        }), 400

    service = SalaService()

    try:
        sala = service.adicionar(**schema)

        return created(
          data=sala.to_dict(),
          mensagem='Sala criada com sucesso',
          location=f'/v1/salas/{sala.id}')

    except Exception:
        return internal_error()


@api_salas_v1.route('/salas/<id>', methods=['PUT'])
def editar_sala(id):
    """Edita uma sala de reunião existente.
    ---
    tags:
      - salas
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Id da Sala de Reunião
      - name: sala
        in: body
        type: object
        required: true
        "schema": {
          "$ref": "#/definitions/EditarSalaSchema"
        }
    definitions:
      EditarSalaSchema:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
    responses:
      200:
        description: A sala foi editada com sucesso
      400:
        description: 400 Bad Request
      404:
        description: A sala informada não foi encontrada
      415:
        description: Media Type não suportado
      500:
        description: Um erro não previsto ocorreu
    """
    if not request.is_json:
        return unsuported_media_type()

    try:
        schema = get_json(EditarSalaSchema(), request.get_json())

    except BadRequestError as bad_req_err:
        return jsonify({
          'errors': bad_req_err.errors,
          'status': bad_req_err.code,
          'mensagem': 'Não foi possível salvar a sala'
        }), 400

    service = SalaService()

    try:
        if service.editar(schema):
            return ok(mensagem="Sala editada com sucesso")

        return not_found(mensagem="Sala não encontrada")

    except Exception:
        return internal_error()


@api_salas_v1.route('/salas/<id>', methods=['DELETE'])
def deletar_sala(id):
    """Remove uma sala de reunião existente.
    ---
    tags:
      - salas
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Id da Sala de Reunião
    definitions:
      EditarSalaSchema:
        type: object
        properties:
          nome:
            type: string
          codigo:
            type:
              string
    responses:
      200:
        description: A sala foi excluída com sucesso
      404:
        description: A sala informada não foi encontrada
      500:
        description: Um erro não previsto ocorreu
    """
    sala_service = SalaService()

    try:
        if sala_service.remover(id):
            return ok(mensagem='Sala removida com sucesso')

        return not_found(mensagem="Sala não encontrada")

    except Exception:
        return internal_error()
