# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from agendamentos.exceptions import AgendamentoExistenteError

from .schemas import (
  AgendaSchema,
  EditarAgendaSchema,
  FiltrarAgendaSchema)
from ..commons import (
    conflict,
    created,
    get_args,
    get_json,
    internal_error,
    not_found,
    ok,
    unsuported_media_type)
from ..exceptions import BadRequestError
from ...services import AgendaService



api_agendamento_v1 = Blueprint('api_agendamento_v1', __name__, url_prefix='/v1') # noqa


@api_agendamento_v1.route('/agendamentos', methods=['GET'])
def listar_salas():
    """Realiza uma busca por agendamentos.
    ---
    tags:
      - agendamentos
    
    responses:
      200:
        description: A consulta foi realizada com sucesso
      500:
        description: Um erro não previsto ocorreu
    """
    service = AgendaService()

    try:
        filtro = get_args(FiltrarAgendaSchema(), request.args)

    except BadRequestError as bad_req_err:
        return jsonify({
          'errors': bad_req_err.errors,
          'status': bad_req_err.code,
          'mensagem': 'Não foi possível salvar o agendamento'
        }), 400

    try:
        salas = service.listar(filtro)

        return ok(data=[sala.to_dict() for sala in salas])

    except Exception:
        return internal_error()


@api_agendamento_v1.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    """Cria um novo agendamento.
    ---
    tags:
      - agendamentos
    parameters:
      - name: agenda
        in: body
        type: object
        required: true
        "schema": {
          "$ref": "#/definitions/AgendaSchema"
        }
    definitions:
      AgendaSchema:
        type: object
        properties:
          inicio:
            type: string
            format: date-time
          fim:
            type: string
            format: date-time
          sala_id:
            type: string
    responses:
      201:
        description: O agendamento foi criado
      400:
        description: 400 Bad Request
      409:
        description: Caso a sala já esteja agendada
      415:
        description: Media Type não suportado
      500:
        description: Um erro não previsto ocorreu
    """
    if not request.is_json:
        return unsuported_media_type()

    try:
        schema = get_json(AgendaSchema(), request.get_json())

    except BadRequestError as bad_req_err:
        return jsonify({
          'errors': bad_req_err.errors,
          'status': bad_req_err.code,
          'mensagem': 'Não foi possível salvar o agendamento'
        }), 400

    service = AgendaService()

    try:
        agenda = service.adicionar(**schema)

        return created(
          data=agenda.to_dict(),
          mensagem='Agendamento criado com sucesso',
          location=f'/v1/agendamentos/{agenda.id}')

    except AgendamentoExistenteError as agendamento_err:
        return conflict(mensagem=str(agendamento_err))

    except Exception:
        return internal_error()


@api_agendamento_v1.route('/agendamentos/<id>', methods=['PUT'])
def editar_agendamento(id):
    """Edita um agendamento existente.
    ---
    tags:
      - agendamentos
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Id do Agendamento
      - name: agendamento
        in: body
        type: object
        required: true
        "schema": {
          "$ref": "#/definitions/EditarAgendaSchema"
        }
    definitions:
      EditarAgendaSchema:
        type: object
        properties:
          inicio:
            type: string
            format: date-time
          fim:
            type: string
            format: date-time
          sala_id:
            type: string
    responses:
      200:
        description: O agendamento foi editado com sucesso
      400:
        description: 400 Bad Request
      404:
        description: O agendamento informada não foi encontrado
      415:
        description: Media Type não suportado
      500:
        description: Um erro não previsto ocorreu
    """
    if not request.is_json:
        return unsuported_media_type()

    try:
        schema = get_json(EditarAgendaSchema(), request.get_json())

    except BadRequestError as bad_req_err:
        return jsonify({
          'errors': bad_req_err.errors,
          'status': bad_req_err.code,
          'mensagem': 'Não foi possível salvar o agendamento'
        }), 400

    service = AgendaService()

    try:
        if service.editar(id, schema):
            return ok(mensagem="Agendamento editado com sucesso")

        return not_found(mensagem="Agendamento não encontrado")

    except Exception:
        return internal_error()


@api_agendamento_v1.route('/agendamentos/<id>', methods=['DELETE'])
def deletar_agendamento(id):
    """Remove um agendamento existente.
    ---
    tags:
      - agendamentos
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Id do Agendamento
    responses:
      200:
        description: O agendamento foi excluído com sucesso
      404:
        description: O agendamento informado não foi encontrado
      500:
        description: Um erro não previsto ocorreu
    """
    service = AgendaService()

    try:
        if service.remover(id):
            return ok(mensagem='Agendamento removido com sucesso')

        return not_found(mensagem="Agendamento não encontrado")

    except Exception:
        return internal_error()
