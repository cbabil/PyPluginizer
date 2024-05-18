# -*- coding: utf-8 -*-
class Test:
    def __init__(self, logger, hooks=None, **kwargs):
        # Assign the logger to an instance variable
        self.logger = logger
        # Assign the hooks to an instance variable
        self.hooks = hooks
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        self.logger.info("Executing plugin")

    def process_results(self):
        self.logger.info("Processing results for plugin")
        self.hooks["json"].trigger()
