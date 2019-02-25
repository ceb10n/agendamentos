# -*- coding: utf-8 -*-
import datetime
import uuid

from .database import db


class Agenda(db.Model):

    __tablename__ = 'agendamentos'

    id = db.Column(db.String(36), default=str(uuid.uuid4()), primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    agendado_em = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow())
    sala_id = db.Column(
        db.String(36),
        db.ForeignKey('salas.id'),
        nullable=False)
    sala = db.relationship(
        'Sala',
        backref=db.backref('agendamentos', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'inicio': self.inicio.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            'fim': self.fim.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            'agendado_em': self.agendado_em.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            'sala_id': self.sala_id,
            'sala': self.sala.to_dict()}
