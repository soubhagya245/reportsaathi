"""Pydantic schemas matching the API contracts."""

from backend.app.schemas.health import HealthResponse
from backend.app.schemas.lab_report import (
    ExtractedLabParameter,
    LabExtractErrorResponse,
    LabExtractResponse,
    LabParameterStatus,
    LabPrintedRange,
)
from backend.app.schemas.medicine import (
    BilingualList,
    BilingualText,
    GovernanceMetadata,
    MedicineCardData,
    MedicineCardResponse,
    MedicineNotFoundResponse,
)
from backend.app.schemas.user import DataPurgeRequest, DataPurgeResponse
from backend.app.schemas.whatsapp import (
    WhatsAppButtonReply,
    WhatsAppChange,
    WhatsAppContact,
    WhatsAppEntry,
    WhatsAppImageBody,
    WhatsAppInteractiveBody,
    WhatsAppMessage,
    WhatsAppMetadata,
    WhatsAppTextMessageBody,
    WhatsAppValue,
    WhatsAppWebhookPayload,
)

__all__ = [
    "WhatsAppMetadata",
    "WhatsAppContact",
    "WhatsAppTextMessageBody",
    "WhatsAppButtonReply",
    "WhatsAppInteractiveBody",
    "WhatsAppImageBody",
    "WhatsAppMessage",
    "WhatsAppValue",
    "WhatsAppChange",
    "WhatsAppEntry",
    "WhatsAppWebhookPayload",
    "BilingualText",
    "BilingualList",
    "GovernanceMetadata",
    "MedicineCardData",
    "MedicineCardResponse",
    "MedicineNotFoundResponse",
    "LabPrintedRange",
    "LabParameterStatus",
    "ExtractedLabParameter",
    "LabExtractResponse",
    "LabExtractErrorResponse",
    "DataPurgeRequest",
    "DataPurgeResponse",
    "HealthResponse",
]
