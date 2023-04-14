from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def consume_message(self, message):
        ...
