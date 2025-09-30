from datetime import datetime

from pydantic import BaseModel, Field


class BloodPressureSchema(BaseModel):
    systolic: int | None = Field(
        ...,
        description="Systolic blood pressure value (may be null). Unit usually 'mmHg'.",
    )
    diastolic: int | None = Field(
        ...,
        description="Diastolic blood pressure value (may be null). Unit usually 'mmHg'.",
    )
    unit: str | None = Field(
        ...,
        description="Unit for blood pressure values, e.g. 'mmHg'.",
    )


class HeartRateSchema(BaseModel):
    value: int | None = Field(
        ...,
        description="Heart rate value in beats per minute (may be null).",
    )
    unit: str | None = Field(
        ...,
        description="Unit for heart rate, typically 'bpm'.",
    )


class OxygenSaturationSchema(BaseModel):
    value: int | None = Field(
        ...,
        description="Oxygen saturation percentage (may be null).",
    )
    unit: str | None = Field(
        ...,
        description="Unit for oxygen saturation, typically '%'.",
    )


class TemperatureSchema(BaseModel):
    value: float | None = Field(
        ..., description="Body temperature value (may be null)."
    )
    unit: str | None = Field(
        ...,
        description="Temperature unit, e.g. '°C'.",
    )


class VitalSignsSchema(BaseModel):
    blood_pressure: BloodPressureSchema = Field(
        ..., description="Blood pressure measurements."
    )
    heart_rate: HeartRateSchema = Field(
        ...,
        description="Heart rate measurement.",
    )
    oxygen_saturation: OxygenSaturationSchema = Field(
        ...,
        description="Oxygen saturation measurement.",
    )
    temperature: TemperatureSchema = Field(
        ...,
        description="Temperature measurement.",
    )


class PatientStatusSchema(BaseModel):
    vital_signs: VitalSignsSchema = Field(
        ...,
        description="Collection of vital signs.",
    )
    symptoms: list[str] = Field(
        ...,
        description="Reported symptoms list.",
    )
    observation: list[str] = Field(
        ...,
        description="Observed findings list.",
    )


class MedicationSchema(BaseModel):
    name: str = Field(
        ...,
        description="Medication name.",
    )
    normalized_name: str | None = Field(
        ...,
        description="Normalized medication name if available.",
    )
    dosage: str | None = Field(
        ...,
        description="Dosage string, e.g. '500 mg'.",
    )
    route: str | None = Field(
        ...,
        description="Administration route, e.g. 'oral', 'IV'.",
    )


class InterventionSchema(BaseModel):
    action_type: str = Field(
        ...,
        description="Type of intervention/action performed.",
    )
    medication: MedicationSchema = Field(
        ...,
        description="Medication details for the intervention.",
    )
    timestamp: datetime | None = Field(
        ...,
        description="Timestamp of intervention in ISO8601 with timezone or null.",
    )


class NursingNoteSchema(BaseModel):
    timestamp: datetime | None = Field(
        ...,
        description="Timestamp of the nursing note in ISO8601 with timezone or null.",
    )
    patient_status: PatientStatusSchema = Field(
        ...,
        description="Patient status snapshot including vitals and symptoms.",
    )
    interventions: list[InterventionSchema] = Field(
        ...,
        description="List of interventions performed.",
    )
    denied_symptoms: list[str] = Field(
        ...,
        description="Symptoms denied by the patient.",
    )
    schema_version: str = Field(
        ...,
        description="Schema version identifier.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0.",
    )
    notes: str | None = Field(
        ...,
        description="Additional free-text notes or null.",
    )
    raw_text: str = Field(
        ...,
        description="Raw extracted text that produced this structured note.",
    )
