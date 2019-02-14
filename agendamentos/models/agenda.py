# -*- coding: utf-8 -*-
import uuid

from ..database import db


class Agenda(db.Model):

    __tablename__ = 'salas'

    id = db.Column(db.String(36), default=str(uuid.uuid4()), primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    sala = db.relationship('Sala', backref='agendamentos')
    id_sala = db.Column(
        db.String(36),
        db.ForeignKey('salas.id'),
        nullable=False)
    id_usuario = db.Column(
        db.String(36),
        db.ForeignKey('usuarios.id'),
        nullable=False)
