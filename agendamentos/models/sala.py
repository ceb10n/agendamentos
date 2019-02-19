# -*- coding: utf-8 -*-
import uuid

from .database import db


class Sala(db.Model):

    __tablename__ = 'salas'

    id = db.Column(db.String(36), default=str(uuid.uuid4()), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(15))

    def __repr__(self):
        return '<Sala %r>' % self.nome

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo}
