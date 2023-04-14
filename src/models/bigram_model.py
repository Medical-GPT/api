from .model import Model
import sys
from pathlib import Path
import torch

# Get the parent folder (project) path
project_folder = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(project_folder))

from chatbot.src.pretraining.model import BigramLanguageModel


class BigramModel(Model):
    def __init__(self, path):
        super().__init__()
        self.load(path)

    def load(self, path):
        self.model, self.encode, self.decode = BigramLanguageModel.load(path)

    def consume_message(self, message):
        enc_context = torch.tensor([self.encode(message)], dtype=torch.long)
        response = self.model.generate(enc_context, max_new_tokens=200)
        return self.decode(response[0].tolist())
