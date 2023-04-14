from .model import Model
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


class GPTModel(Model):
    def __init__(self, path, query_string="", response_string=""):
        super().__init__()
        self.load(path)
        self.query_string = query_string
        self.response_string = response_string

    def load(self, path):
        self.model = GPT2LMHeadModel.from_pretrained(path)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        self.model.eval()

    def consume_message(self, message):
        adjusted_message = f"{self.query_string} {message}\n{self.response_string}"
        input_ids = self.tokenizer.encode(adjusted_message, return_tensors="pt")
        attention_mask = torch.ones_like(input_ids)
        output = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=200,
            do_sample=True,
            top_k=50,
            temperature=0.6,
        )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        print(generated_text)

        # Clear the response
        if self.response_string != "":
            generated_text = generated_text.split(self.response_string)[-1]

        # Trim the query
        # if len(generated_text) > 300:
        generated_text = ".".join(generated_text.split(".")[:4])

        return generated_text
