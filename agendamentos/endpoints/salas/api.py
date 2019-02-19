# -*- coding: utf-8 -*-
from flask import Blueprint, abort, jsonify, request

from ..commons import get_json, created, ok, not_found, unsuported_media_type
from ..exceptions import BadRequestError
from ...models import Sala, db
from ...services import SalaService
from .schemas import EditarSalaSchema, SalaSchema


api_salas_v1 = Blueprint('api_salas_v1', __name__, url_prefix='/v1')


@api_salas_v1.route('/salas/<id>', methods=['GET'])
def pesquisar_sala(id):
    service = SalaService()
    sala = service.procurar_por_id(id)

    if sala:
        return ok(data=sala.to_dict())

    return not_found('Sala não encontrada')


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
    sala = service.adicionar(**schema)

    return created(
      data=sala.to_dict(),
      mensagem='Sala criada com sucesso',
      location=f'/v1/salas/{sala.id}')


@api_salas_v1.route('/salas/<id>', methods=['PUT'])
def editar_sala(id):
    if not request.is_json:
        return unsuported_media_type()

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


@api_salas_v1.route('/salas/<id>', methods=['DELETE'])
def deletar_sala(id):
    sala = Sala.query.get(id)

    db.session.delete(sala)
    db.session.commit()

    return 'ok', 201
