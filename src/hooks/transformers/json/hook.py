# -*- coding: utf-8 -*-
class JsonExporter:
    def __init__(self, logger, **kwargs):
        self.logger = logger
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def trigger(self):
        self.logger.info('Executing JsonExporter hook...')
