import pytest
from app.analytics.service import AnalyticsService


def test_domain_detection_sales():
    domain = AnalyticsService._detect_domain(["order_id", "sales_amount", "customer_name"])
    assert domain == "Sales"


def test_domain_detection_hr():
    domain = AnalyticsService._detect_domain(["employee_id", "salary", "department"])
    assert domain == "HR"
