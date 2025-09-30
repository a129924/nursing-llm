from dataclasses import dataclass
from datetime import datetime

"""
{
  "timestamp": "string|null",         // ISO8601 with timezone or null
  "patient_status": {
    "vital_signs": {
      "blood_pressure": { "systolic": number|null, "diastolic": number|null, "unit": "mmHg"|null },
      "heart_rate": { "value": number|null, "unit": "bpm"|null },
      "oxygen_saturation": { "value": number|null, "unit": "%"|null },
      "temperature": { "value": number|null, "unit": "°C"|null }
    },
    "symptoms": [ "string" ],
    "observation": [ "string" ]
  },
  "interventions": [
    {
      "action_type": "string",
      "medication": { "name": "string", "normalized_name": "string|null", "dosage": "string|null", "route": "string|null" },
      "timestamp": "string|null"
    }
  ],
  "denied_symptoms": [ "string" ],
  "schema_version": "string",
  "confidence": number,               // 0.0 - 1.0
  "notes": "string|null",
  "raw_text": "string"
}
"""


@dataclass(frozen=True)
class BloodPressure:
    systolic: int | None
    diastolic: int | None
    unit: str | None  # e.g., "mmHg"


@dataclass(frozen=True)
class HeartRate:
    value: int | None
    unit: str | None  # e.g., "bpm"


@dataclass(frozen=True)
class OxygenSaturation:
    value: int | None
    unit: str | None  # e.g., "%"


@dataclass(frozen=True)
class Temperature:
    value: float | None
    unit: str | None  # e.g., "°C"


@dataclass(frozen=True)
class VitalSigns:
    blood_pressure: BloodPressure
    heart_rate: HeartRate
    oxygen_saturation: OxygenSaturation
    temperature: Temperature


@dataclass(frozen=True)
class PatientStatus:
    vital_signs: VitalSigns
    symptoms: list[str]
    observation: list[str]


@dataclass(frozen=True)
class Medication:
    name: str
    normalized_name: str | None
    dosage: str | None
    route: str | None


@dataclass(frozen=True)
class Intervention:
    action_type: str
    medication: Medication
    timestamp: datetime | None  # ISO8601 with timezone or null


@dataclass(frozen=True)
class NursingNote:
    timestamp: datetime | None  # ISO8601 with timezone or null
    patient_status: PatientStatus
    interventions: list[Intervention]
    denied_symptoms: list[str]
    schema_version: str
    confidence: float
    notes: str | None
    raw_text: str
