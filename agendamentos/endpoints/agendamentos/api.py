# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from ..commons import unsuported_media_type
from ...models import Agenda, db
from .schemas import EditarAgendaSchema, AgendaSchema

api_agendamento_v1 = Blueprint('api_agendamento_v1', __name__, url_prefix='/v1') # noqa


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
      415:
        description: Media Type não suportado
      500:
        description: Um erro não previsto ocorreu
    """
    if not request.is_json:
        return unsuported_media_type()

    agenda_schema = AgendaSchema()
    schema = agenda_schema.load(request.get_json())

    agenda = Agenda(**schema)

    db.session.add(agenda)
    db.session.commit()

    return 'ok', 201


@api_agendamento_v1.route('/agendamentos/<id>', methods=['PUT'])
def editar_sala(id):
    if request.is_json:
        agenda_schema = EditarAgendaSchema()
        schema = agenda_schema.load(request.get_json())

        agenda = Agenda.query.get(id)

        if 'inicio' in schema and schema['inicio']:
            agenda.inicio = schema['inicio']

        if 'fim' in schema and schema['fim']:
            agenda.fim = schema['fim']

        if 'sala_id' in schema and schema['sala_id']:
            agenda.sala_id = schema['sala_id']

        db.session.add(agenda)
        db.session.commit()

        return 'ok', 201

    return jsonify({
        'error': '415 Unsupported Media Type',
        'message': 'Media Type não suportado',
        'code': 415
    }), 415


@api_agendamento_v1.route('/agendamentos/<id>', methods=['DELETE'])
def deletar_agendamento(id):
    agenda = Agenda.query.get(id)

    db.session.delete(agenda)
    db.session.commit()

    return 'ok', 201
