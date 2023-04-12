from model import Model
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GPTModel(Model):
    def __init__(self, path):
        super().__init__(path)

    def load(self, path):
        self.model = GPT2LMHeadModel.from_pretrained(path)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.tokenizer.add_special_tokens({"pad_token": "[PAD]"})
        self.model.eval()

    def consume_message(self, message):
        input_ids = self.tokenizer.encode(message, return_tensors="pt")
        output = self.model.generate(
            input_ids=input_ids,
            max_length=100,
            do_sample=True,
            top_k=50,
            temperature=0.05,
        )

        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text
