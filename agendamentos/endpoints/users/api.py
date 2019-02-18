# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request

from ...models import Usuario, db
from .schemas import UsuarioSchema

api_usuarios_v1 = Blueprint('api_usuarios_v1', __name__, url_prefix='/v1')


@api_usuarios_v1.route('/usuarios')
def criar_usuario():
    if request.is_json:
        usuario_schema = UsuarioSchema()
        schema = usuario_schema.load(request.get_json())
        usuario = Usuario(**schema)
        usuario.criar_senha(schema['senha'])
        db.session.add(usuario)
        db.session.commit()

        return 'ok', 201

    return jsonify({
        'error': '415 Unsupported Media Type',
        'message': 'Media Type não suportado',
        'code': 415
    }), 415
