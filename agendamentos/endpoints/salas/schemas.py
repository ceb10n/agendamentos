# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate


class SalaSchema(Schema):

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

    codigo = fields.Str(
        required=True,
        allow_none=False,
        validate=[
            validate.Length(
                min=2,
                max=15,
                error='O código deve conter entre 2 e 15 caracteres')],
        error_messages={
            'required': 'O código é obrigatório',
            'null': 'O código não pode ser nulo'})


class EditarSalaSchema(Schema):

    nome = fields.Str(
        allow_none=True,
        validate=[
            validate.Length(
                min=2,
                max=100,
                error='O nome deve conter entre 2 e 100 caracteres')])

    codigo = fields.Str(
        allow_none=True,
        validate=[
            validate.Length(
                min=2,
                max=15,
                error='O código deve conter entre 2 e 15 caracteres')])
