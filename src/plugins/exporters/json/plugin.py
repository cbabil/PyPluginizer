class JsonExporter:
    def __init__(self, **kwargs):
        # Assign each value from kwargs to an instance variable
        for key, value in kwargs.items():
            setattr(self, key, value)

    def execute(self):
        self.logger.info("Executing Json exporter plugin")

    def process_results(self):
        self.logger.info("Processing results for Json exporter plugin")
