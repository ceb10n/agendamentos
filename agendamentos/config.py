# -*- coding: utf-8 -*-
import logging
import os

from dotenv import load_dotenv
from flasgger import Swagger


def init_logs(app):
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info('Logs configurados')


def init_env(app, ambiente=None):
    app.logger.info('Iniciando variaveis de ambiente')
    load_dotenv()

    app.logger.info('Verificando ambiente')

    if not ambiente:
        ambiente = os.getenv("AMBIENTE")

    app.config['TESTING'] = ambiente == 'test'
    app.config['DEBUG'] = ambiente == 'development'
    app.config['ENV'] = ambiente

    app.logger.info('Ambiente %s definido' % (app.config['ENV']))


def init_swagger(app):
    app.logger.info('Iniciando Swagger')
    swagger = Swagger(app)

    return swagger
