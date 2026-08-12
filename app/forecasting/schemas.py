from typing import Any

from pydantic import BaseModel, Field


class ForecastRequest(BaseModel):
    target_column: str = Field(..., description="Target numerical column to forecast")
    date_column: str | None = Field(None, description="Date/time column")
    horizon_periods: int = Field(5, ge=1, le=100)
    model_name: str = Field("auto", description="auto, moving_average, exponential_smoothing, prophet, xgboost")


class ForecastResponse(BaseModel):
    target_column: str
    selected_model: str
    mae: float
    rmse: float
    mape: float
    confidence_interval: dict[str, float]
    forecast_values: list[dict[str, Any]]
