from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self):
        self.load()

    @abstractmethod
    def load(self):
        ...

    @abstractmethod
    def consume_message(self, message):
        ...
