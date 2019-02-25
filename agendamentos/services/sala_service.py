# -*- coding: utf-8 -*-
import uuid

from agendamentos.logs import get_logger

from ..models import db, Sala


class SalaService:
    """Serviço para operações e manipulações das salas de reuniões."""

    def __init__(self, *args, **kwargs):
        self.logger = get_logger()

    def procurar_por_id(self, id):
        self.logger.info('SalaService: procurando sala de reunião com o id {id}.') # noqa
        return Sala.query.get(id)

    def listar(self):
        self.logger.info('SalaService: listando todas as salas de reunião.') # noqa
        return Sala.query.all()

    def adicionar(self, **data):
        self.logger.info('SalaService: adicionando uma nova sala de reunião.') # noqa
        sala = Sala(**data)
        sala.id = str(uuid.uuid4())

        db.session.add(sala)
        db.session.commit()

        return sala

    def editar(self, id, data):
        self.logger.info('SalaService: editado a sala de reunião com id {id}.') # noqa
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
        self.logger.info('SalaService: removendo a sala de reunião com id {id}.') # noqa
        sala = Sala.query.get(id)

        if not sala:
            self.logger.info('SalaService: a sala de reunião com id {id} não foi removida pois era inexistente.') # noqa
            return False

        db.session.delete(sala)
        db.session.commit()

        return True
