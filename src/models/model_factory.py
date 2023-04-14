import json
from .bigram_model import BigramModel
from .gpt_model import GPTModel
from .gpt_specialized import GPTMedicalModel, GPTEmpathicModel
from .model_chain import ModelChain


class ModelFactory:
    def __init__(self):
        # Open the models.json file and read its contents
        with open("src/models/models.json", "r") as f:
            models_json = f.read()
        with open("src/models/chains.json", "r") as f:
            chains_json = f.read()

        self.models, self.models_info = self.load_models(json.loads(models_json))
        chains, chains_info = self.load_chains(json.loads(chains_json))

        self.models.update(chains)
        self.models_info.extend(chains_info)

    def load_models(self, models_json):
        models = {}
        models_info = []
        for name, model in models_json.items():
            if model["type"] == "bigram":
                model_type = BigramModel
            elif model["type"] == "gpt2":
                model_type = GPTModel
            elif model["type"] == "gpt2-medical":
                model_type = GPTMedicalModel
            elif model["type"] == "gpt2-empathic":
                model_type = GPTEmpathicModel
            else:
                raise Exception("Invalid model type")

            models[name] = model_type(model["path"])
            if model["interface"]:
                models_info.append({"model": name, "alias": model["alias"]})

        return models, models_info

    def load_chains(self, chains_json):
        chains = {}
        chains_info = []
        for name, chain in chains_json.items():
            chains[name] = ModelChain(self.get_models(chain["models"]))
            if chain["interface"]:
                chains_info.append({"model": name, "alias": chain["alias"]})
        return chains, chains_info

    def consume(self, message):
        text = message["message"]
        model_name = message["model"]
        return self.models[model_name].consume_message(text)

    def get_models(self, models):
        return [self.models[model] for model in models]

    def get_models_json(self):
        return self.models_info
