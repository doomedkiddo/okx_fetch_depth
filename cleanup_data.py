from clickhouse_driver import Client
from datetime import datetime, timedelta

# ClickHouse client
client = Client('localhost', user='default', password='kali')

# Calculate the date 7 days ago
seven_days_ago = datetime.now() - timedelta(days=7)

# Delete data older than 7 days
query = f"""
DELETE FROM okx_doge_usdt_swap
WHERE Timestamp < '{seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')}'
"""

client.execute(query)

print("Data cleanup completed.")
