爬取okx五档深度以及价格数据，存入clickhouse数据库

# sql clickhouse
 CREATE TABLE default.okx_doge_usdt_swap
(
    `Timestamp` DateTime,
    `Last_Price` Float64,
    `Last_Size` Float64,
    `Ask0_Price` Float64,
    `Ask0_Volume` Float64,
    `Ask1_Price` Float64,
    `Ask1_Volume` Float64,
    `Ask2_Price` Float64,
    `Ask2_Volume` Float64,
    `Ask3_Price` Float64,
    `Ask3_Volume` Float64,
    `Ask4_Price` Float64,
    `Ask4_Volume` Float64,
    `Bid0_Price` Float64,
    `Bid0_Volume` Float64,
    `Bid1_Price` Float64,
    `Bid1_Volume` Float64,
    `Bid2_Price` Float64,
    `Bid2_Volume` Float64,
    `Bid3_Price` Float64,
    `Bid3_Volume` Float64,
    `Bid4_Price` Float64,
    `Bid4_Volume` Float64
)
ENGINE = MergeTree
ORDER BY Timestamp
TTL Timestamp + toIntervalDay(7)
SETTINGS index_granularity = 8192 



