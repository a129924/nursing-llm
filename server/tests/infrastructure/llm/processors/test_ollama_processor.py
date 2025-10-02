from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.llm.processors.ollama_processor import (
    OllamaProcessor,
)


def test_ollama_processor_instantiation(
    ollama_processor: OllamaProcessor, full_ollama_response: str
) -> None:
    assert isinstance(ollama_processor, OllamaProcessor)
    assert ollama_processor is not None

    assert ollama_processor.validate_and_map(full_ollama_response) is not None
    assert isinstance(
        ollama_processor.validate_and_map(full_ollama_response), NursingNote
    )
