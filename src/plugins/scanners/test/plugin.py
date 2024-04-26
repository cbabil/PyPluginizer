import logging

logger = logging.getLogger(__name__)


class Test:
    def __init__(self, **kwargs):
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        logger.info("Executing Test plugin")

    def process_results(self):
        logger.info("Processing results for Test plugin")

    def hook_method(self, *args, **kwargs):
        logger.info("Hook method called in MyPlugin")
