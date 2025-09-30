from typing_extensions import override

from nursing_llm_server.core.shared.mapper import PydanticModelMapperABC
from nursing_llm_server.domain.entities.nursing import (
    Intervention,
    NursingNote,
    PatientStatus,
)
from nursing_llm_server.infrastructure.entities.nursing import NursingNoteSchema


class NursingMapper(PydanticModelMapperABC[NursingNoteSchema, NursingNote]):
    @override
    def schema_to_entity(self, schema: NursingNoteSchema) -> NursingNote:
        return NursingNote(
            timestamp=schema.timestamp,
            patient_status=PatientStatus(**schema.patient_status.model_dump()),
            interventions=[
                Intervention(**intervention.model_dump())
                for intervention in schema.interventions
            ],
            denied_symptoms=schema.denied_symptoms,
            schema_version=schema.schema_version,
            confidence=schema.confidence,
            notes=schema.notes,
            raw_text=schema.raw_text,
        )
