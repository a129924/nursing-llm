from typing_extensions import override

from nursing_llm_server.core.shared.mapper import PydanticModelMapperABC
from nursing_llm_server.domain.entities.nursing import (
    BloodPressure,
    HeartRate,
    Intervention,
    Medication,
    NursingNote,
    OxygenSaturation,
    PatientStatus,
    Temperature,
    VitalSigns,
)
from nursing_llm_server.infrastructure.entities.nursing import (
    MedicationSchema,
    NursingNoteSchema,
    VitalSignsSchema,
)


class NursingMapper(PydanticModelMapperABC[NursingNoteSchema, NursingNote]):
    def _vital_signs_to_entity(self, vital_sign_schema: VitalSignsSchema) -> VitalSigns:
        return VitalSigns(
            blood_pressure=BloodPressure(
                **vital_sign_schema.blood_pressure.model_dump()
            ),
            heart_rate=HeartRate(**vital_sign_schema.heart_rate.model_dump()),
            oxygen_saturation=OxygenSaturation(
                **vital_sign_schema.oxygen_saturation.model_dump()
            ),
            temperature=Temperature(**vital_sign_schema.temperature.model_dump()),
        )

    def _patient_status_to_entity(self, schema: NursingNoteSchema) -> PatientStatus:
        return PatientStatus(
            vital_signs=self._vital_signs_to_entity(schema.patient_status.vital_signs),
            symptoms=schema.patient_status.symptoms,
            observation=schema.patient_status.observation,
        )

    def _medication_to_entity(self, medication_schema: MedicationSchema) -> Medication:
        return Medication(
            name=medication_schema.name,
            normalized_name=medication_schema.normalized_name,
            dosage=medication_schema.dosage,
            route=medication_schema.route,
        )

    @override
    def schema_to_entity(self, schema: NursingNoteSchema) -> NursingNote:
        return NursingNote(
            timestamp=schema.timestamp,
            patient_status=self._patient_status_to_entity(schema),
            interventions=[
                Intervention(
                    action_type=intervention.action_type,
                    medication=self._medication_to_entity(intervention.medication),
                    timestamp=intervention.timestamp,
                )
                for intervention in schema.interventions
            ],
            denied_symptoms=schema.denied_symptoms,
            schema_version=schema.schema_version,
            confidence=schema.confidence,
            notes=schema.notes,
            raw_text=schema.raw_text,
        )
