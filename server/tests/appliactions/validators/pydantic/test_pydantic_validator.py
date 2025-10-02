from datetime import datetime, timedelta, timezone

from pytest import raises

from nursing_llm_server.applications.validators.errors import ValidationError
from nursing_llm_server.applications.validators.pydantic.pydantic_validator import (
    PydanticValidator,
)
from nursing_llm_server.infrastructure.entities.nursing import (
    BloodPressureSchema,
    HeartRateSchema,
    NursingNoteSchema,
    OxygenSaturationSchema,
    TemperatureSchema,
)
from nursing_llm_server.infrastructure.llm.schemas import OllamaGenerateResponseSchema


def test_valid_ollama_response_schema(
    valid_easy_ollama_response_schema: OllamaGenerateResponseSchema,
):
    assert valid_easy_ollama_response_schema.model == "ollama/llama2"
    assert valid_easy_ollama_response_schema.done is True
    assert len(valid_easy_ollama_response_schema.context) == 2
    assert valid_easy_ollama_response_schema.total_duration == 1.23
    assert valid_easy_ollama_response_schema.eval_count == 2
    assert valid_easy_ollama_response_schema.response == "這是一個測試回應。"


def test_valid_fuzzy_ollama_response_schema(
    valid_fuzzy_nursing_record_schema: NursingNoteSchema,
):
    assert valid_fuzzy_nursing_record_schema.timestamp is None
    assert (
        valid_fuzzy_nursing_record_schema.patient_status.vital_signs.temperature
        == TemperatureSchema(value=None, unit="°C")
    )
    assert (
        valid_fuzzy_nursing_record_schema.patient_status.vital_signs.blood_pressure
        == BloodPressureSchema(systolic=None, diastolic=None, unit="mmHg")
    )
    assert (
        valid_fuzzy_nursing_record_schema.patient_status.vital_signs.heart_rate
        == HeartRateSchema(value=None, unit="bpm")
    )
    assert (
        valid_fuzzy_nursing_record_schema.patient_status.vital_signs.oxygen_saturation
        == OxygenSaturationSchema(value=None, unit="%")
    )
    assert valid_fuzzy_nursing_record_schema.patient_status.symptoms == []
    assert valid_fuzzy_nursing_record_schema.interventions == []
    assert valid_fuzzy_nursing_record_schema.denied_symptoms == []
    assert valid_fuzzy_nursing_record_schema.schema_version == "1.0"
    assert valid_fuzzy_nursing_record_schema.confidence == 0.35
    assert (
        valid_fuzzy_nursing_record_schema.notes
        == "No measurable vitals, medications, or specific symptoms/times found; cannot extract structured fields."
    )
    assert (
        valid_fuzzy_nursing_record_schema.raw_text
        == "病人狀況不佳，請加強注意並回報異常情形。"
    )


def test_valid_nursing_record_schema(
    valid_nursing_record_schema: NursingNoteSchema,
):
    assert valid_nursing_record_schema.timestamp == datetime(
        2025, 9, 25, 7, 30, tzinfo=timezone(timedelta(hours=8))
    )  # "2025-09-25T07:30:00+08:00"
    assert (
        valid_nursing_record_schema.patient_status.vital_signs.temperature
        == TemperatureSchema(value=None, unit="°C")
    )
    assert (
        valid_nursing_record_schema.patient_status.vital_signs.blood_pressure
        == BloodPressureSchema(systolic=150, diastolic=90, unit="mmHg")
    )
    assert (
        valid_nursing_record_schema.patient_status.vital_signs.heart_rate
        == HeartRateSchema(value=None, unit="bpm")
    )
    assert (
        valid_nursing_record_schema.patient_status.vital_signs.oxygen_saturation
        == OxygenSaturationSchema(value=None, unit="%")
    )
    assert valid_nursing_record_schema.patient_status.symptoms == ["頭痛", "噁心"]
    assert len(valid_nursing_record_schema.interventions) == 0
    assert valid_nursing_record_schema.denied_symptoms == []
    assert valid_nursing_record_schema.schema_version == "1.0"
    assert valid_nursing_record_schema.confidence == 0.9
    assert valid_nursing_record_schema.notes is None
    assert (
        valid_nursing_record_schema.raw_text
        # == "病人主訴頭痛及發燒，血壓120/80 mmHg，心率75 bpm，血氧98%。給予退燒藥物並建議多休息。無噁心或嘔吐症狀。"
        == "病患今晨血壓 150/90 mmHg，頭痛。2025-09-25 07:30 覺得噁心。"
    )


def test_error_json_format(
    error_json_format: str, pydantic_validator: PydanticValidator
):
    with raises(ValidationError):
        pydantic_validator.validate(OllamaGenerateResponseSchema, error_json_format)
