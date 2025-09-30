from dataclasses import dataclass
from datetime import datetime
from typing import Annotated


@dataclass(frozen=True)
class LLMResponse:
    """大型語言模型回應數據傳輸對象"""

    model: Annotated[str, "使用的模型名稱"]
    created_at: Annotated[datetime, "創建時間"]
    response: Annotated[str, "模型回應"]
    done: Annotated[bool, "是否完成"]
    eval_count: Annotated[int, "評估次數"]
    total_duration: Annotated[float, "總耗時（秒）"]
    load_duration: Annotated[float, "模型加載時間（秒）"]
