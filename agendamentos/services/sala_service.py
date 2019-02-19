# -*- coding: utf-8 -*-
from ..models import db, Sala


class SalaService:

    def procurar_por_id(self, id):
        return Sala.query.get(id)

    def listar(self):
        return Sala.query.all()

    def adicionar(self, **data):
        sala = Sala(**data)
        db.session.add(sala)
        db.session.commit()

        return sala

    def editar(self, data):
        sala = Sala.query.get(id)

        if not sala:
            return False

        if 'nome' in data and data['nome']:
            sala.nome = data['nome']

        if 'codigo' in data and data['codigo']:
            sala.codigo = data['codigo']

        db.session.add(sala)
        db.session.commit()

        return True

    def remover(self, id):
        sala = Sala.query.get(id)

        if not sala:
            return False

        db.session.delete(sala)
        db.session.commit()

        return True
