from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from nursing_llm_server.core.enums.role import Role


class OllamaGenerateResponseSchema(BaseModel):
    """Ollama API 回應模型。"""

    model: str = Field(..., description="使用的模型名稱")
    created_at: datetime = Field(..., description="回應創建時間")
    response: str = Field(..., description="模型生成的回應文本")
    done: bool = Field(..., description="請求是否完成")
    context: list[str] = Field(..., description="上下文信息")
    total_duration: float = Field(..., description="請求總耗時（秒）")
    load_duration: float = Field(..., description="模型加載時間（秒）")
    prompt_eval_count: int = Field(..., description="提示評估計數")
    prompt_eval_duration: float = Field(..., description="提示評估耗時（秒）")
    eval_count: int = Field(..., description="評估計數")
    eval_duration: float = Field(..., description="評估耗時（秒）")


class ChatMessageSchema(BaseModel):
    """訊息物件，包含角色與內容。"""

    role: Role = Field(..., description="訊息角色，例如 Role.ASSISTANT 或 Role.USER")
    content: str = Field(..., description="訊息內容")

    @field_validator("role", mode="before")
    @classmethod
    def _parse_role(cls, v):
        if isinstance(v, Role):
            return v
        if isinstance(v, str):
            # accept case-insensitive names like "assistant" or "ASSISTANT"
            try:
                return Role[v.upper()]
            except KeyError:
                mapping = {r.name.lower(): r for r in Role}
                if v.lower() in mapping:
                    return mapping[v.lower()]
        raise ValueError(f"Invalid role: {v}")


class OllamaChatResponseSchema(BaseModel):
    """
    ```json
        {
        "model": "llama2:7b-chat",
        "created_at": "2025-10-01T08:44:25.304513Z",
        "message": {
            "role": "assistant",
            "content": ""
        },
        "done": true,
        "done_reason": "stop",
        "total_duration": 39475704292,
        "load_duration": 637248209,
        "prompt_eval_count": 2738,
        "prompt_eval_duration": 14289012000,
        "eval_count": 528,
        "eval_duration": 24535051208
    }
    ```
    Ollama Chat API 回應模型。
    """

    model: str = Field(..., description="使用的模型名稱")
    created_at: datetime = Field(..., description="回應創建時間")
    message: ChatMessageSchema = Field(..., description="回傳的訊息物件，含角色與內容")
    done: bool = Field(..., description="請求是否完成")
    done_reason: str = Field(..., description="完成原因，例如 'stop' 或其他")
    total_duration: float = Field(..., description="請求總耗時（秒）")
    load_duration: float = Field(..., description="模型加載時間（秒）")
    prompt_eval_count: int = Field(..., description="提示評估計數")
    prompt_eval_duration: float = Field(..., description="提示評估耗時（秒）")
    eval_count: int = Field(..., description="評估計數")
    eval_duration: float = Field(..., description="評估耗時（秒）")
