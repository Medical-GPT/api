import json
from .bigram_model import BigramModel
from .gpt_model import GPTModel


class ModelFactory:
    def __init__(self):
        # Open the models.json file and read its contents
        with open("src/models/models.json", "r") as f:
            json_data = f.read()

        # Parse the JSON data into a Python dictionary
        models_json = json.loads(json_data)
        self.models = self.load_models(models_json)

    def load_models(self, models_json):
        models = {}
        for name, model in models_json.items():
            if model["type"] == "bigram":
                model_type = BigramModel
            elif model["type"] == "gpt2":
                model_type = GPTModel
            else:
                raise Exception("Invalid model type")

            models[name] = model_type(model["path"])

        return models

    def consume(self, message):
        text = message["message"]
        model_name = message["model"]
        return self.models[model_name].consume_message(text)