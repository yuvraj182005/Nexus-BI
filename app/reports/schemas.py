from typing import Any

from pydantic import BaseModel, Field


class ReportGenerateRequest(BaseModel):
    report_type: str = Field("executive", description="executive, business, analytics, forecast, data_quality")
    title: str = Field("Decision Intelligence Summary Report")
    format: str = Field("markdown", description="markdown, html, pdf_json, docx_json, ppt_json")


class ReportGenerateResponse(BaseModel):
    report_id: str
    report_type: str
    title: str
    format: str
    rendered_content: str | dict[str, Any]
