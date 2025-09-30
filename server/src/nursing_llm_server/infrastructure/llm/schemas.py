from datetime import datetime

from pydantic import BaseModel, Field


class OllamaResponseSchema(BaseModel):
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
