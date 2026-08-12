from typing import Any

from pydantic import BaseModel, Field


class NotificationSendRequest(BaseModel):
    channel: str = Field("email", description="email, slack, webhook")
    recipient: str = Field(..., description="Target email address, Slack channel ID, or webhook URL")
    subject: str | None = Field(None, description="Subject line for email")
    body: str = Field(..., description="Notification body message")


class NotificationSendResponse(BaseModel):
    notification_id: str
    channel: str
    recipient: str
    status: str
    delivery_logs: dict[str, Any]
