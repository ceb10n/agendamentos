# -*- coding: utf-8 -*-
import uuid

from sqlalchemy import Date, DateTime, cast, and_, or_

from agendamentos.exceptions import AgendamentoExistenteError
from agendamentos.logs import get_logger

from ..models import db, Agenda, Sala


class AgendaService:
    """Serviço para operações e manipulações dos agendamentos."""

    def __init__(self, *args, **kwargs):
        self.logger = get_logger()

    def procurar_por_id(self, id):
        self.logger.info('AgendaService: procurando agendamento com o id {id}')
        return Agenda.query.get(id)

    def listar(self, filtros):
        self.logger.info('AgendaService: realizando filtro dos agendamentos')

        try:
            query = Agenda.query

            if 'data' in filtros and filtros['data']:
                self.logger.info(f'AgendaService: filtrando agendamentos pela data: {filtros["data"]}') # noqa

                query = query.filter(
                    cast(Agenda.inicio, Date) == filtros['data'])

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
            self.logger.info('AgendaService: Um agendamento foi cancelado por tentar marcar no mesmo horário que outro agendamento existente.') # noqa
            raise AgendamentoExistenteError('A sala já está reservada neste horário') # noqa

        agendamento = Agenda(**data)
        agendamento.id = str(uuid.uuid4())

        db.session.add(agendamento)
        db.session.commit()

        return agendamento

    def editar(self, id, data):
        self.logger.info(f'AgendaService: O agendamento com id {id} está sendo editado') # noqa

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
        self.logger.info(f'AgendaService: O agendamento com id {id} será removido') # noqa

        agendamento = Agenda.query.get(id)

        if not agendamento:
            self.logger.info(f'AgendaService: O agendamento com id {id} não foi removido pois era inexistente') # noqa
            return False

        db.session.delete(agendamento)
        db.session.commit()

        return True

    def existe_agendamento(self, inicio, fim, sala_id):
        query = Agenda.query.filter(Agenda.sala_id == sala_id)

        query = query.filter(
            or_(
                and_(
                    (cast(Agenda.inicio, DateTime) >= inicio),
                    (cast(Agenda.inicio, DateTime) <= fim)),
                and_(
                    (cast(Agenda.fim, DateTime) <= inicio),
                    (cast(Agenda.fim, DateTime) >= fim))))

        return len(query.all()) > 0
