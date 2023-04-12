from .model import Model
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


class GPTModel(Model):
    def __init__(self, path):
        super().__init__(path)

    def load(self, path):
        self.model = GPT2LMHeadModel.from_pretrained(path)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        self.model.eval()

    def consume_message(self, message):
        adjusted_message = f"Patient: {message}\nDoctor:"
        input_ids = self.tokenizer.encode(adjusted_message, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)
        output = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=100,
            do_sample=True,
            top_k=50,
            temperature=0.6,
        )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        trimmed = generated_text.split("Doctor: ")[-1]

        if len(trimmed) > 300:
            trimmed = ".".join(trimmed.split(".")[:-1])

        return trimmed
