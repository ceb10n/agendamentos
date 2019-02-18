# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, validate


class AgendaSchema(Schema):

    inicio = fields.DateTime(
        required=True,
        allow_none=False,
        error_messages={
            'required': 'O início do agendamento é obrigatório',
            'null': 'O início do agendamento não pode ser nulo'})

    fim = fields.Str(
        required=True,
        allow_none=False,
        error_messages={
            'required': 'O fim do agendamento é obrigatório',
            'null': 'O fim do agendamento não pode ser nulo'})

    sala_id = fields.Str(
        required=True,
        allow_none=False,
        validate=[
            validate.Length(
                min=36,
                max=36,
                error='O id deve ser um uuid de 36 caracteres')],
        error_messages={
            'required': 'O id da sala é obrigatório',
            'null': 'O id da sala não pode ser nulo'})


class EditarAgendaSchema(Schema):

    inicio = fields.DateTime(allow_none=True)
    fim = fields.Str(allow_none=True)
    sala_id = fields.Str(
        allow_none=True,
        validate=[
            validate.Length(
                min=36,
                max=36,
                error='O id deve ser um uuid de 36 caracteres')])
