# -*- coding: utf-8 -*-
import os

from flask import Flask

from config import init_env, init_logs, init_swagger
from database import db


def init_app():
    app = Flask(__name__)
    
    init_logs(app)
    init_env(app)
    init_swagger(app)
    db.init_app(app)

    return app


if __name__ == '__main__':
    # a porta padrão do servidor embutido do Flask é 5000.
    # Caso seja necessário rodar em uma outra porta, basta criar a variável
    # de ambiente APP_PORTA com a porta desejada.
    porta = os.getenv('APP_PORTA', 5000)

    app = init_app()

    app.run(debug=True, port=int(porta), host='0.0.0.0')
