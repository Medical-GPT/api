from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, path):
        self.load(path)

    @abstractmethod
    def load(self, path):
        ...

    @abstractmethod
    def consume_message(self, message):
        ...
