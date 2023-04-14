from .gpt_model import GPTModel


class GPTMedicalModel(GPTModel):
    def __init__(self, path):
        super().__init__(path, "Patient:", "Doctor:")


class GPTEmpathicModel(GPTModel):
    def __init__(self, path):
        super().__init__(path, "Original:", "Empathic:")
