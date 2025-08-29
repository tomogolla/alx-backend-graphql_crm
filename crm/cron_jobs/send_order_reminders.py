#!/usr/bin/env python3
import sys
import os
import logging
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Configure logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def main():
    try:
        # GraphQL endpoint
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Calculate date range (last 7 days)
        today = datetime.utcnow().date()
        last_week = today - timedelta(days=7)

        # GraphQL query
        query = gql("""
        query GetPendingOrders($startDate: Date!, $endDate: Date!) {
            orders(orderDate_Gte: $startDate, orderDate_Lte: $endDate) {
                id
                customer {
                    email
                }
            }
        }
        """)

        # Run query with variables
        params = {
            "startDate": str(last_week),
            "endDate": str(today),
        }
        result = client.execute(query, variable_values=params)

        # Log results
        for order in result.get("orders", []):
            order_id = order.get("id")
            customer_email = order.get("customer", {}).get("email")
            logging.info(f"Reminder for Order {order_id}, Customer: {customer_email}")

        print("Order reminders processed!")

    except Exception as e:
        logging.error(f"Error processing order reminders: {e}")
        print(f"Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
