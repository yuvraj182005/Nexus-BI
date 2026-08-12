import pytest
from app.notifications.schemas import NotificationSendRequest
from app.reports.schemas import ReportGenerateRequest


def test_report_schema():
    req = ReportGenerateRequest(report_type="executive", format="markdown")
    assert req.report_type == "executive"


def test_notification_schema():
    req = NotificationSendRequest(channel="email", recipient="admin@example.com", body="Alert body")
    assert req.recipient == "admin@example.com"
