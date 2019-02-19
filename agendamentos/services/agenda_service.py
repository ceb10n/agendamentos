# -*- coding: utf-8 -*-
from ..models import db, Agenda


class AgendaService:
    """Serviço para operações e manipulações dos agendamentos."""

    def procurar_por_id(self, id):
        return Agenda.query.get(id)

    def listar(self):
        return Agenda.query.all()

    def adicionar(self, **data):
        agendamento = Agenda(**data)
        db.session.add(agendamento)
        db.session.commit()

        return agendamento

    def editar(self, data):
        agendamento = Agenda.query.get(id)

        if not agendamento:
            return False

        if 'inicio' in data and data['inicio']:
            agendamento.inicio = data['inicio']

        if 'fim' in data and data['fim']:
            agendamento.fim = data['fim']

        if 'sala_id' in data and data['sala_id']:
            agendamento.sala_id = data['sala_id']

        db.session.add(agendamento)
        db.session.commit()

        return True

    def remover(self, id):
        agendamento = Agenda.query.get(id)

        if not agendamento:
            return False

        db.session.delete(agendamento)
        db.session.commit()

        return True
