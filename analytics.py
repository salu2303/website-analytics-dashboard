from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account
import json
from dotenv import load_dotenv
import os

load_dotenv()
credentials_path = os.getenv("GA4_CREDENTIALS_PATH")

def get_device_stats(config):
    credentials = service_account.Credentials.from_service_account_file(
        config["ga4"]["credentials_path"]
    )
    client = BetaAnalyticsDataClient(credentials=credentials)
    start = config.get("date_range", {}).get("start_date", "7daysAgo")
    end = config.get("date_range", {}).get("end_date", "today")

    request = RunReportRequest(
        property=f"properties/{config['ga4']['property_id']}",
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date=start, end_date=end)]
        # date_ranges=[DateRange(start_date="2025-04-22", end_date="2025-04-29")]
        # date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
    )

    response = client.run_report(request)
    device_stats = {row.dimension_values[0].value: row.metric_values[0].value for row in response.rows}
    return device_stats


def get_custom_page_views(config):
    credentials = service_account.Credentials.from_service_account_file(
        config["ga4"]["credentials_path"]
    )
    client = BetaAnalyticsDataClient(credentials=credentials)
    start = config.get("date_range", {}).get("start_date", "7daysAgo")
    end = config.get("date_range", {}).get("end_date", "today")

    paths = [
        "/",  # homepage
        "/my-account/education-webinars/",
        "/my-account/monographs/",
        "/insider-scoop/"
    ]

    request = RunReportRequest(
        property=f"properties/{config['ga4']['property_id']}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimension_filter={
            "filter": {
                "field_name": "pagePath",
                "in_list_filter": {"values": paths}
            }
        }
    )

    response = client.run_report(request)

    results = {}
    for row in response.rows:
        path = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        results[path] = views

    return results
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from google.oauth2 import service_account

def get_top_product_page_views(config):
    credentials = service_account.Credentials.from_service_account_file(config["ga4"]["credentials_path"])
    client = BetaAnalyticsDataClient(credentials=credentials)
    start = config.get("date_range", {}).get("start_date", "7daysAgo")
    end = config.get("date_range", {}).get("end_date", "today")

    request = RunReportRequest(
        property=f"properties/{config['ga4']['property_id']}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimension_filter={
            "filter": {
                "field_name": "pagePath",
                "string_filter": {
                    "match_type": "BEGINS_WITH",
                    "value": "/product/",
                    "case_sensitive": False
                }
            }
        }
    )

    response = client.run_report(request)

    # Collect and sort top 10 product pages
    pages = []
    for row in response.rows:
        path = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        pages.append((path, views))

    top_10 = sorted(pages, key=lambda x: x[1], reverse=True)[:10]
    return top_10

def get_total_website_users(config):
    credentials = service_account.Credentials.from_service_account_file(
        config["ga4"]["credentials_path"]
    )
    client = BetaAnalyticsDataClient(credentials=credentials)
    start = config.get("date_range", {}).get("start_date", "7daysAgo")
    end = config.get("date_range", {}).get("end_date", "today")

    request = RunReportRequest(
        property=f"properties/{config['ga4']['property_id']}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        metrics=[Metric(name="activeUsers")]
    )

    response = client.run_report(request)
    return int(response.rows[0].metric_values[0].value)

from google.analytics.data_v1beta.types import Dimension

def create_ga4_client(config):
    credentials = service_account.Credentials.from_service_account_file(config["ga4"]["credentials_path"])
    return BetaAnalyticsDataClient(credentials=credentials)


def get_last_search_terms(config):
    client = create_ga4_client(config)
    start = config.get("date_range", {}).get("start_date", "7daysAgo")
    end = config.get("date_range", {}).get("end_date", "today")
    request = RunReportRequest(
        property=f"properties/{config['ga4']['property_id']}",
        dimensions=[Dimension(name="searchTerm")],
        metrics=[Metric(name="eventCount")],  # fallback metric
        date_ranges=[DateRange(start_date=start, end_date=end)]
    )
    response = client.run_report(request)

    search_terms = []
    for row in response.rows:
        term = row.dimension_values[0].value
        if term:  # ignore blank search terms
            search_terms.append(term)

    # Return last 10 terms (or fewer if not enough)
    return search_terms[:11]



