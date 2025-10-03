from abc import ABC, abstractmethod


class AIPlatformUrlBuilderABC(ABC):
    @abstractmethod
    def build_chat_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_generate_url(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_health_url(self) -> str:
        raise NotImplementedError
