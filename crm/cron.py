import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client
import logging


def log_crm_heartbeat():
    """
    Logs a heartbeat message every 5 minutes to confirm CRM is alive.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)


def heartbeat_logger():
    logging.info("Heartbeat job executed")

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",  # adjust if needed
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )

    result = client.execute(query)
    logging.info(f"GraphQL heartbeat: {result}")



def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    result = client.execute(mutation)
    updated_products = result["updateLowStockProducts"]["updatedProducts"]

    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"\n[{datetime.datetime.now()}] Updated products:\n")
        for product in updated_products:
            f.write(f"- {product['name']}: {product['stock']}\n")
