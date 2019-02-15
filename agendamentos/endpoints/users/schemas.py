# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate


class UsuarioSchema(Schema):

    nome = fields.Str(
        required=True,
        allow_none=False,
        validate=[
            validate.Length(
                min=2,
                max=100,
                error='O nome deve conter entre 2 e 100 caracteres')],
        error_messages={
            'required': 'O nome é obrigatório',
            'null': 'O nome não pode ser nulo'})

    email = fields.Str(
        required=True,
        allow_none=False,
        validate=[
            validate.Email(
                error='O e-mail informado não é válido'),
            validate.Length(
                min=7,
                max=100,
                error='O e-mail deve conter entre 7 e 100 caracteres')],
        error_messages={
            'required': 'O e-mail é obrigatório',
            'null': 'O e-mail não pode ser nulo'})

    senha = fields.Str(
        required=True,
        allow_none=False,
        load_only=True,
        validate=[
            validate.Length(
                min=6,
                max=50,
                error='A senha deve conter entre 6 e 50 caracteres')],
        error_messages={
            'required': 'A senha é obrigatória'})