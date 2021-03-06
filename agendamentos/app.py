# -*- coding: utf-8 -*-
import os

from flask import Flask

from agendamentos.config import (
    init_db,
    init_env,
    init_logs,
    init_sentry,
    init_swagger)
from agendamentos.models import db
from agendamentos.endpoints.agendamentos import api_agendamento_v1
from agendamentos.endpoints.salas import api_salas_v1


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config['TESTING'] = True
    else:
        init_env(app)
        init_logs(app)
        init_sentry(app)
        init_swagger(app)

    init_db(app)
    db.init_app(app)

    app.register_blueprint(api_agendamento_v1)
    app.register_blueprint(api_salas_v1)

    return app


if __name__ == '__main__':
    # a porta padrão do servidor embutido do Flask é 5000.
    # Caso seja necessário rodar em uma outra porta, basta criar a variável
    # de ambiente APP_PORTA com a porta desejada.
    porta = os.getenv('APP_PORTA', 5000)

    app = create_app()

    # rota adicionada apenas para facilitar a criação inicial do banco de
    # dados, ou resetar o banco para fins de teste durante o desenvolvimento
    @app.route('/resetdb')
    def resetdb():
        """Destroys and creates the database + tables."""
        DB_URL = os.getenv('SQLALCHEMY_DATABASE_URI', default='sqlite://')

        from sqlalchemy_utils import (
            database_exists,
            create_database,
            drop_database)

        if database_exists(DB_URL):
            drop_database(DB_URL)

        if not database_exists(DB_URL):
            create_database(DB_URL)

        db.create_all()

        return "ok", 200

    app.run(debug=True, port=int(porta), host='0.0.0.0')
