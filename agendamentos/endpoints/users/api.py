# -*- coding: utf-8 -*-
from flask import Blueprint, request

from .schemas import UsuarioSchema

api_usuarios_v1 = Blueprint('api_usuarios_v1', __name__, '/v1')



@api_usuarios_v1.route('/users', methods=['POST'])
def criar_usuario():
    usuario_schema = UsuarioSchema()    
    schema = usuario_schema.load(request.get_json()).data
    return "", 200
    # user = User(**schema)
    # user.gen_hash()

    # db.session.add(user)
    # db.session.commit()

    # return jsonify({
    #     'message': 'User {} created!'.format(user.email)
    # }), 201