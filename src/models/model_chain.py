from .model import Model


class ModelChain(Model):
    def __init__(self, models):
        self.models = models

    def consume_message(self, message):
        response = message
        for model in self.models:
            response = model.consume_message(response)
        return response
