from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WhatsAppProfile(BaseModel):
    name: str


class WhatsAppContact(BaseModel):
    profile: WhatsAppProfile
    wa_id: str


class WhatsAppTextMessageBody(BaseModel):
    body: str


class WhatsAppButtonReply(BaseModel):
    id: str
    title: str


class WhatsAppInteractiveBody(BaseModel):
    type: Literal["button_reply"] = "button_reply"
    button_reply: WhatsAppButtonReply


class WhatsAppImageBody(BaseModel):
    id: str
    mime_type: str
    sha256: str


class WhatsAppMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    type: Literal["text", "interactive", "image"]
    text: WhatsAppTextMessageBody | None = None
    interactive: WhatsAppInteractiveBody | None = None
    image: WhatsAppImageBody | None = None


class WhatsAppValue(BaseModel):
    messaging_product: Literal["whatsapp"]
    metadata: WhatsAppMetadata
    contacts: list[WhatsAppContact] | None = None
    messages: list[WhatsAppMessage] | None = None


class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str = "messages"


class WhatsAppEntry(BaseModel):
    id: str
    changes: list[WhatsAppChange]


class WhatsAppWebhookPayload(BaseModel):
    object: Literal["whatsapp_business_account"]
    entry: list[WhatsAppEntry]
