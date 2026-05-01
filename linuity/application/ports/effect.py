from abc import ABC, abstractmethod


class Effect(ABC):
    @abstractmethod
    def execute(self, preset: dict) -> None:
        pass
