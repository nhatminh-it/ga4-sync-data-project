from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension

def fetch_ga4_data(property_id, credentials, start_date="7daysAgo", end_date="yesterday"):
    """
    Fetch data from GA4 API using the specified property ID and credentials.
    """
    client = BetaAnalyticsDataClient(credentials=credentials)
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date"), Dimension(name="country")],
        metrics=[
            Metric(name="clicks"),
            Metric(name="spend"),
            Metric(name="sales"),
            Metric(name="conversions")
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )
    response = client.run_report(request)
    return response.rows
