# -*- coding: utf-8 -*-
import json

from flask import Blueprint, jsonify, request

from ..commons import get_json, created
from ..exceptions import BadRequestError
from ...models import Sala, db
from .schemas import EditarSalaSchema, SalaSchema


api_salas_v1 = Blueprint('api_salas_v1', __name__, url_prefix='/v1')


@api_salas_v1.route('/salas', methods=['POST'])
def criar_sala():
    """Endpoint para criação de novas salas de reunião.

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
    """
    if request.is_json:
        try:
            schema = get_json(SalaSchema(), request.get_json())

        except BadRequestError as bad_req_err:
            return jsonify({
              'errors': bad_req_err.errors,
              'status': bad_req_err.code,
              'mensagem': 'Não foi possível salvar a sala'
            }), 400

        sala = Sala(**schema)
        db.session.add(sala)
        db.session.commit()

        created(data=json.dumps(sala), mensagem='Sala criada com sucesso')

    return jsonify({
        'error': '415 Unsupported Media Type',
        'message': 'Media Type não suportado',
        'code': 415
    }), 415


@api_salas_v1.route('/salas/<id>', methods=['PUT'])
def editar_sala(id):
    if request.is_json:
        sala_schema = EditarSalaSchema()
        schema = sala_schema.load(request.get_json())

        sala = Sala.query.get(id)

        if 'nome' in schema and schema['nome']:
            sala.nome = schema['nome']

        if 'codigo' in schema and schema['codigo']:
            sala.codigo = schema['codigo']

        db.session.add(sala)
        db.session.commit()

        return 'ok', 201

    return jsonify({
        'error': '415 Unsupported Media Type',
        'message': 'Media Type não suportado',
        'code': 415
    }), 415


@api_salas_v1.route('/salas/<id>', methods=['DELETE'])
def deletar_sala(id):
    sala = Sala.query.get(id)

    db.session.delete(sala)
    db.session.commit()

    return 'ok', 201
