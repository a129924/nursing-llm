from abc import ABC, abstractmethod


class Loader(ABC):
    @abstractmethod
    def load(self) -> dict:
        raise NotImplementedError("請在子類別中實作此方法")
