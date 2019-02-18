# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from ...models import Agenda, db
from .schemas import EditarAgendaSchema, AgendaSchema

api_agendamento_v1 = Blueprint('api_agendamento_v1', __name__, url_prefix='/v1')


@api_agendamento_v1.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    if request.is_json:
        agenda_schema = AgendaSchema()
        schema = agenda_schema.load(request.get_json())
        import uuid
        sala = Agenda(**schema)
        sala.id = str(uuid.uuid4())

        db.session.add(sala)
        db.session.commit()

        return 'ok', 201

    return jsonify({
        'error': '415 Unsupported Media Type',
        'message': 'Media Type não suportado',
        'code': 415
    }), 415


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
