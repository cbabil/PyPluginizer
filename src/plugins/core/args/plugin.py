# -*- coding: utf-8 -*-
class Args:
    def __init__(self, **kwargs):
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        self.logger.info('Executing Args plugin...')

    def process_results(self, results):
        self.logger.info('Processing results for Args plugin')
