# -*- coding: utf-8 -*-
import uuid

from .database import db


class Agenda(db.Model):

    __tablename__ = 'agendamentos'

    id = db.Column(db.String(36), default=str(uuid.uuid4()), primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
