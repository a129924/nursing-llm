from typing_extensions import override

from nursing_llm_server.applications.dto.llm_response import LLMResponse
from nursing_llm_server.core.shared.mapper import PydanticModelMapperABC
from nursing_llm_server.infrastructure.llm.schemas import OllamaGenerateResponseSchema


class OllamaLLMResponseMapper(
    PydanticModelMapperABC[OllamaGenerateResponseSchema, LLMResponse]
):
    @override
    def schema_to_entity(self, schema: OllamaGenerateResponseSchema) -> LLMResponse:
        return LLMResponse(
            model=schema.model,
            created_at=schema.created_at,
            response=schema.response,
            done=schema.done,
            eval_count=schema.eval_count,
            total_duration=schema.total_duration,
            load_duration=schema.load_duration,
        )
