# -*- coding: utf-8 -*-
from ..models import db, Sala


class SalaService:

    def adicionar(self, **data):
        sala = Sala(**data)
        db.session.add(sala)
        db.session.commit()

        return sala
