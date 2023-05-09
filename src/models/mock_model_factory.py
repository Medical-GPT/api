from .model_factory import ModelFactory


class MockModelFactory(ModelFactory):
    def __init__(self):
        super().__init__()

    def consume(self, message):
        return "mock response"
