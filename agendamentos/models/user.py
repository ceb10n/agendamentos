# -*- coding: utf-8 -*-
import uuid

from passlib.hash import bcrypt

from ..database import db


class Usuario(db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(db.String(36), default=str(uuid.uuid4()), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    agendamentos = db.relationship('Agenda', backref='agendado_por')

    def criar_senha(self, senha):
        self.senha = bcrypt.hash(senha)

    def senha_valida(self, senha):
        return bcrypt.verify(senha, self.senha)

    def __repr__(self):
        return '<User %r>' % self.email