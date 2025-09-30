from datetime import datetime, timedelta, timezone

from nursing_llm_server.domain.entities.nursing import NursingNote
from nursing_llm_server.infrastructure.entities.nursing import NursingNoteSchema
from nursing_llm_server.infrastructure.llm.adapters.mappers.pydantic.nursing_mapper import (
    NursingMapper,
)


def test_nursing_mapper_with_fuzzy_nursing_record_schema(
    fuzzy_nursing_record_json: str,
) -> None:
    schema = NursingNoteSchema.model_validate_json(fuzzy_nursing_record_json)
    entity = NursingMapper().schema_to_entity(schema)

    assert entity.timestamp is None
    assert entity.patient_status.vital_signs.blood_pressure.systolic is None
    assert entity.patient_status.vital_signs.blood_pressure.diastolic is None
    assert entity.patient_status.vital_signs.blood_pressure.unit == "mmHg"
    assert entity.patient_status.vital_signs.heart_rate.value is None
    assert entity.patient_status.vital_signs.heart_rate.unit == "bpm"
    assert entity.patient_status.vital_signs.oxygen_saturation.value is None
    assert entity.patient_status.vital_signs.oxygen_saturation.unit == "%"
    assert entity.patient_status.vital_signs.temperature.value is None
    assert entity.patient_status.vital_signs.temperature.unit == "°C"
    assert entity.patient_status.symptoms == []
    assert entity.patient_status.observation == []
    assert entity.interventions == []
    assert entity.denied_symptoms == []
    assert entity.schema_version == "1.0"
    assert entity.confidence == 0.35
    assert (
        entity.notes
        == "No measurable vitals, medications, or specific symptoms/times found; cannot extract structured fields."
    )
    assert entity.raw_text == "病人狀況不佳，請加強注意並回報異常情形。"


def test_nursing_mapper_with_nursing_record_schema(
    mapped_nursing_note: NursingNote,
) -> None:
    assert mapped_nursing_note.timestamp == datetime(
        2025, 9, 25, 7, 30, tzinfo=timezone(timedelta(hours=8))
    )  # "2025-09-25T07:30:00+08:00"
    assert mapped_nursing_note.patient_status.vital_signs.blood_pressure.systolic == 150
    assert mapped_nursing_note.patient_status.vital_signs.blood_pressure.diastolic == 90
    assert mapped_nursing_note.patient_status.vital_signs.blood_pressure.unit == "mmHg"
    assert mapped_nursing_note.patient_status.vital_signs.heart_rate.value is None
    assert mapped_nursing_note.patient_status.vital_signs.heart_rate.unit == "bpm"
    assert (
        mapped_nursing_note.patient_status.vital_signs.oxygen_saturation.value is None
    )
    assert mapped_nursing_note.patient_status.vital_signs.oxygen_saturation.unit == "%"
    assert mapped_nursing_note.patient_status.vital_signs.temperature.value is None
    assert mapped_nursing_note.patient_status.vital_signs.temperature.unit == "°C"
    assert mapped_nursing_note.patient_status.symptoms == ["頭痛", "噁心"]
    assert mapped_nursing_note.patient_status.observation == []
    assert mapped_nursing_note.interventions == []
    assert mapped_nursing_note.denied_symptoms == []
    assert mapped_nursing_note.schema_version == "1.0"
    assert mapped_nursing_note.confidence == 0.9
    assert mapped_nursing_note.notes is None
    assert (
        mapped_nursing_note.raw_text
        == "病患今晨血壓 150/90 mmHg，頭痛。2025-09-25 07:30 覺得噁心。"
    )
