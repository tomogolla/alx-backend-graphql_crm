import logging
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

logger = logging.getLogger(__name__)

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """
    )

    result = client.execute(query)
    customers = result.get("totalCustomers", 0)
    orders = result.get("totalOrders", 0)
    revenue = result.get("totalRevenue", 0)

    log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

    with open("/tmp/crm_report_log.txt", "a") as log_file:
        log_file.write(log_message)

    logger.info(log_message)
