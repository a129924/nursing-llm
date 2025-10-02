from typing import cast

from pytest import fixture

from nursing_llm_server.applications.validators.pydantic.pydantic_validator import (
    PydanticValidator,
)
from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.entities.nursing import (
    NursingNoteSchema,
)
from nursing_llm_server.infrastructure.llm.adapters.mappers.pydantic.nursing_mapper import (
    NursingMapper,
)
from nursing_llm_server.infrastructure.llm.processors.ollama_processor import (
    OllamaProcessor,
)
from nursing_llm_server.infrastructure.llm.schemas import OllamaResponseSchema


@fixture(scope="module")
def easy_ollama_response_json() -> str:
    return """{
    "model": "ollama/llama2",
    "created_at": "2023-08-30T12:00:00Z",
    "response": "這是一個測試回應。",
    "done": true,
    "context": ["上下文信息1", "上下文信息2"],
    "total_duration": 1.23,
    "load_duration": 0.45,
    "prompt_eval_count": 3,
    "prompt_eval_duration": 0.67,
    "eval_count": 2,
    "eval_duration": 0.89
}"""


@fixture(scope="module")
def fuzzy_nursing_record_json() -> str:
    return """
{
            "timestamp": null,
            "patient_status": {
                "vital_signs": {
                    "blood_pressure": {
                        "systolic": null,
                        "diastolic": null,
                        "unit": "mmHg"
                    },
                    "heart_rate": {
                        "value": null,
                        "unit": "bpm"
                    },
                    "oxygen_saturation": {
                        "value": null,
                        "unit": "%"
                    },
                    "temperature": {
                        "value": null,
                        "unit": "°C"}
                },
                "symptoms": [],
                "observation": []
            },
            "interventions": [],
            "denied_symptoms": [],
            "schema_version": "1.0",
            "confidence": 0.35,
            "notes": "No measurable vitals, medications, or specific symptoms/times found; cannot extract structured fields.",
            "raw_text": "病人狀況不佳，請加強注意並回報異常情形。"
        }
"""


@fixture(scope="module")
def nursing_record_json() -> str:
    return """{
            "timestamp": "2025-09-25T07:30:00+08:00",
            "patient_status": {
                "vital_signs": {
                    "blood_pressure": {
                        "systolic": 150,
                        "diastolic": 90,
                        "unit": "mmHg"
                    },
                    "heart_rate": {
                        "value": null,
                        "unit": "bpm"
                    },
                    "oxygen_saturation": {
                        "value": null,
                        "unit": "%"
                    },
                    "temperature": {
                        "value": null,
                        "unit": "°C"
                    }
                },
                "symptoms": [
                    "頭痛",
                    "噁心"
                ],
                "observation": []
            },
            "interventions": [],
            "denied_symptoms": [],
            "schema_version": "1.0",
            "confidence": 0.9,
            "notes": null,
            "raw_text": "病患今晨血壓 150/90 mmHg，頭痛。2025-09-25 07:30 覺得噁心。"
        }"""


@fixture(scope="module")
def full_ollama_response(nursing_record_json: str) -> str:
    from json import dumps

    return dumps(
        {
            "model": "ollama/llama2",
            "created_at": "2023-08-30T12:00:00Z",
            "response": f"{nursing_record_json}",
            "done": True,
            "context": ["上下文信息1", "上下文信息2"],
            "total_duration": 1.23,
            "load_duration": 0.45,
            "prompt_eval_count": 3,
            "prompt_eval_duration": 0.67,
            "eval_count": 2,
            "eval_duration": 0.89,
        }
    )


@fixture(scope="module")
def error_json_format() -> str:
    return """{{
    "model": "ollama/llama2",
    "created_at": "2023-08-30T12:00:00Z",
    "response": "這是一個測試回應。",
    "done": true,
    "context": ["上下文信息1", "上下文信息2"],
    "total_duration": 1.23,
    "load_duration": 0.45,
    "prompt_eval_count": 3,
    "prompt_eval_duration": 0.67,
    "eval_count": 2,
    "eval_duration": 0.89
}"""


@fixture(scope="module")
def pydantic_validator() -> PydanticValidator:
    return PydanticValidator()


@fixture(scope="module")
def valid_easy_ollama_response_schema(
    easy_ollama_response_json: str, pydantic_validator: PydanticValidator
) -> OllamaResponseSchema:
    return cast(
        OllamaResponseSchema,
        pydantic_validator.validate(OllamaResponseSchema, easy_ollama_response_json),
    )


@fixture(scope="module")
def valid_fuzzy_nursing_record_schema(
    fuzzy_nursing_record_json: str, pydantic_validator: PydanticValidator
) -> NursingNoteSchema:
    return cast(
        NursingNoteSchema,
        pydantic_validator.validate(NursingNoteSchema, fuzzy_nursing_record_json),
    )


@fixture(scope="module")
def valid_nursing_record_schema(
    nursing_record_json: str, pydantic_validator: PydanticValidator
) -> NursingNoteSchema:
    return cast(
        NursingNoteSchema,
        pydantic_validator.validate(NursingNoteSchema, nursing_record_json),
    )


@fixture(scope="module")
def nursing_mapper() -> NursingMapper:
    return NursingMapper()


@fixture(scope="module")
def mapped_nursing_note(
    nursing_mapper: NursingMapper,
    valid_nursing_record_schema: NursingNoteSchema,
) -> NursingNote:
    return nursing_mapper.schema_to_entity(valid_nursing_record_schema)


@fixture(scope="module")
def ollama_processor(
    pydantic_validator: PydanticValidator,
    nursing_mapper: NursingMapper,
) -> OllamaProcessor:
    return OllamaProcessor(
        validator=pydantic_validator,
        payload_mapper=nursing_mapper,
    )
