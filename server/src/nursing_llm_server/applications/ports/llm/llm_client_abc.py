from abc import ABC, abstractmethod


class LLMClientABC(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """根據輸入的提示詞生成回應。

        Args:
            prompt (str): 用於生成回應的提示詞。

        Returns:
            str: 生成的回應。
        """
        raise NotImplementedError("Subclasses must implement this method.")
