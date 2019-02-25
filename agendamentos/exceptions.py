# -*- coding: utf-8 -*-
class AgendamentoExistenteError(Exception):

    def __init__(self, *args, **kwargs):
        super(AgendamentoExistenteError, self).__init__(*args, **kwargs)
