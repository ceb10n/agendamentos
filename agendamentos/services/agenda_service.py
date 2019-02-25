# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import func

from ..models import db, Agenda, Sala

from agendamentos.logs import get_logger


class AgendaService:
    """Serviço para operações e manipulações dos agendamentos."""

    def __init__(self, *args, **kwargs):
        self.logger = get_logger()

    def procurar_por_id(self, id):
        return Agenda.query.get(id)

    def listar(self, filtros):
        self.logger.info('AgendaService: realizando filtro dos agendamentos')

        try:
            query = Agenda.query

            if 'data' in filtros and filtros['data']:
                self.logger.info(f'AgendaService: filtrando agendamentos pela data: {filtros["data"]}') # noqa

                query = query.filter(
                    func.date(Agenda.inicio) == func.date(filtros['data']))

            if 'sala_id' in filtros and filtros['sala_id']:
                self.logger.info(f'AgendaService: filtrando agendamentos pela sala: {filtros["sala_id"]}') # noqa
                query = query.filter(Agenda.sala_id == filtros['sala_id'])

            return query.all()
        except Exception as ex:
            self.logger.error(f'AgendaService: erro ao realizar o filtro dos agendamentos') # noqa
            self.logger.error(str(ex))

            raise Exception('AgendaService: erro ao realizar o filtro dos agendamentos') from ex # noqa

    def adicionar(self, **data):
        if 'sala_id' not in data:
            raise Exception('O id da sala é obrigatório')

        if Sala.query.get(data['sala_id']) is None:
            raise Exception('A sala deve ser válida')

        ja_existe_agendamento = self.existe_agendamento(
            data['inicio'],
            data['fim'],
            data['sala_id'])

        if ja_existe_agendamento:
            raise Exception('A sala já está reservada neste horário')

        agendamento = Agenda(**data)
        agendamento.id = str(uuid.uuid4())

        db.session.add(agendamento)
        db.session.commit()

        return agendamento

    def editar(self, id, data):
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

    def existe_agendamento(self, inicio, fim, sala_id):
        return any(Agenda.query.filter(
            Agenda.sala_id == sala_id,
            Agenda.inicio >= inicio,
            Agenda.fim <= inicio,
            Agenda.inicio >= fim,
            Agenda.fim >= fim))
