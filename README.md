# OKX DOGE/USDT Swap Data Scraper

This project scrapes OKX's DOGE/USDT swap data, including the five-level depth and price data, and stores it in a ClickHouse database.

## Table of Contents

- [SQL ClickHouse Table Creation](#sql-clickhouse-table-creation)
- [Cron Job Setup](#cron-job-setup)

## SQL ClickHouse Table Creation

The following SQL script creates a table in ClickHouse to store the OKX DOGE/USDT swap data.

```sql
-- Create a table to store OKX DOGE/USDT swap data
CREATE TABLE default.okx_doge_usdt_swap
(
    `Timestamp` DateTime,          -- Timestamp of the data entry
    `Last_Price` Float64,          -- Last traded price
    `Last_Size` Float64,           -- Last traded size
    `Ask0_Price` Float64,          -- Best ask price (level 0)
    `Ask0_Volume` Float64,         -- Best ask volume (level 0)
    `Ask1_Price` Float64,          -- Ask price (level 1)
    `Ask1_Volume` Float64,         -- Ask volume (level 1)
    `Ask2_Price` Float64,          -- Ask price (level 2)
    `Ask2_Volume` Float64,         -- Ask volume (level 2)
    `Ask3_Price` Float64,          -- Ask price (level 3)
    `Ask3_Volume` Float64,         -- Ask volume (level 3)
    `Ask4_Price` Float64,          -- Ask price (level 4)
    `Ask4_Volume` Float64,         -- Ask volume (level 4)
    `Bid0_Price` Float64,          -- Best bid price (level 0)
    `Bid0_Volume` Float64,         -- Best bid volume (level 0)
    `Bid1_Price` Float64,          -- Bid price (level 1)
    `Bid1_Volume` Float64,         -- Bid volume (level 1)
    `Bid2_Price` Float64,          -- Bid price (level 2)
    `Bid2_Volume` Float64,         -- Bid volume (level 2)
    `Bid3_Price` Float64,          -- Bid price (level 3)
    `Bid3_Volume` Float64,         -- Bid volume (level 3)
    `Bid4_Price` Float64,          -- Bid price (level 4)
    `Bid4_Volume` Float64          -- Bid volume (level 4)
)
ENGINE = MergeTree
ORDER BY Timestamp
TTL Timestamp + toIntervalDay(7)
SETTINGS index_granularity = 8192;
```
## Cron Job Setup
To automate the data cleanup process, you can set up a cron job. The following command sets up a cron job to run a Python script daily at midnight.

```bash
# Edit the crontab file to add a new cron job
crontab -e

# Add the following line to run the cleanup script daily at midnight
0 0 * * * /path/to/your/venv/bin/python /path/to/your/cleanup_data.py
```
### Additional Notes
Ensure that the Python script cleanup_data.py is correctly implemented and located at the specified path.

