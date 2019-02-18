# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from ...models import Sala, db
from .schemas import EditarSalaSchema, SalaSchema

api_salas_v1 = Blueprint('api_salas_v1', __name__, url_prefix='/v1')


@api_salas_v1.route('/salas', methods=['POST'])
def criar_sala():
    """Endpoint para criação de novas salas de reunião.

    ---
    parameters:
      - name: sala
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    if request.is_json:
        sala_schema = SalaSchema()
        schema = sala_schema.load(request.get_json())
        sala = Sala(**schema)

        db.session.add(sala)
        db.session.commit()

        return 'ok', 201

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
