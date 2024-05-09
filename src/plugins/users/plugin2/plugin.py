# -*- coding: utf-8 -*-
class Test1:
    def __init__(self, **kwargs):
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        self.logger.info('Executing Test1 plugin')

    def process_results(self, results):
        self.logger.info('Processing results for Test1 plugin')
