from .model import Model
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re


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

    def get_sentances(self, text):
        splitted = re.split("(\. |\? )", text)

        ret = []

        for idx in range(0, len(splitted), 2):
            if idx == len(splitted) - 1:
                ret.append(splitted[idx])
                break
            ret.append(splitted[idx] + splitted[idx + 1][:-1])
        return ret

    def is_sentances_same(self, sentance1, sentance2, min_repeating_characters=15):
        for chunk_start in range(
            0,
            len(sentance2),
            min_repeating_characters,
        ):
            chunk = sentance2[chunk_start : chunk_start + min_repeating_characters]
            if chunk in sentance1:
                return True
        return False

    def trim_repeating_sentances(self, text, min_repeating_characters=15):
        sentances = self.get_sentances(text)
        ret = []
        for idx, sentance in enumerate(sentances):
            for prev_sentance in sentances[:idx]:
                if self.is_sentances_same(
                    sentance, prev_sentance, min_repeating_characters
                ):
                    break
            else:
                ret.append(sentance)
                continue
            break
        return " ".join(ret)

    def clear_message(self, message):
        # Clear the response
        if self.response_string == "":
            return message
        return message.split(f"{self.response_string} ")[-1]

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

        # Clear the response
        generated_text = self.clear_message(generated_text)

        # Remove repeating sentences
        generated_text = self.trim_repeating_sentances(generated_text)

        print(f"Response: {generated_text}")
        print()
        return generated_text
