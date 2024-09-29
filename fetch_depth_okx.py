import websocket
import json
from datetime import datetime
import time
from clickhouse_driver import Client

# Global variables to store the last price and last size of BTC-USDT
last_price_btc_usdt = None
last_size_btc_usdt = None

# ClickHouse client
client = Client('localhost', user='default', password='kali')  # 替换为你的 ClickHouse 服务器地址

# Function to handle incoming messages
def on_message(ws, message):
    global last_price_btc_usdt, last_size_btc_usdt

    data = json.loads(message)

    if 'data' in data and data['arg']['channel'] == 'tickers':
        last_price_btc_usdt = data['data'][0]['last']
        last_size_btc_usdt = data['data'][0]['lastSz']
        print(f"Updated BTC-USDT last price to {last_price_btc_usdt} and last size to {last_size_btc_usdt}")

    elif 'data' in data and data['arg']['channel'] == 'books5':
        timestamp = datetime.now()
        bids = data['data'][0]['bids'][:5]
        asks = data['data'][0]['asks'][:5]
        row = [timestamp]  # 第一个元素是 timestamp，保持不变
        row.append(float(last_price_btc_usdt if last_price_btc_usdt else 'N/A'))
        row.append(float(last_size_btc_usdt if last_size_btc_usdt else 'N/A'))
        
        for ask in asks:
            row.extend([float(x) for x in ask[:2]])  # 将 ask 中的前两个元素转换为 float

        for bid in bids:
            row.extend([float(x) for x in bid[:2]])  # 将 bid 中的前两个元素转换为 float
        # Insert data into ClickHouse
        client.execute(
            'INSERT INTO okx_doge_usdt_swap (Timestamp, Last_Price, Last_Size, Ask0_Price, Ask0_Volume, Ask1_Price, Ask1_Volume, Ask2_Price, Ask2_Volume, Ask3_Price, Ask3_Volume, Ask4_Price, Ask4_Volume, Bid0_Price, Bid0_Volume, Bid1_Price, Bid1_Volume, Bid2_Price, Bid2_Volume, Bid3_Price, Bid3_Volume, Bid4_Price, Bid4_Volume) VALUES',
            [tuple(row)],
            types_check=True
        )
        print(f"Data written for {timestamp}")

# Function to handle WebSocket errors
def on_error(ws, error):
    print(f"Error: {error}")

# Function to handle WebSocket closure
def on_close(ws):
    print("### Connection Closed ###")

# Function to handle WebSocket opening
def on_open(ws):
    print("### Connection Opened ###")
    subscribe_messages = [
        {
            "op": "subscribe",
            "args": [
                {
                    "channel": "books5",
                    "instId": "DOGE-USDT-SWAP"
                }
            ]
        },
        {
            "op": "subscribe",
            "args": [
                {
                    "channel": "tickers",
                    "instId": "DOGE-USDT-SWAP"
                }
            ]
        }
    ]

    for message in subscribe_messages:
        ws.send(json.dumps(message))

# Main function
if __name__ == "__main__":
    while True:
        try:
            websocket.enableTrace(True)
            ws = websocket.WebSocketApp("wss://ws.okx.com:8443/ws/v5/public",
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open
            ws.run_forever(ping_interval=60, ping_timeout=10)
        except KeyboardInterrupt:
            print('Terminating the program...')
            raise SystemExit
        except Exception as e:
            print(f"Exception: {e}. Attempting to reconnect in 10 seconds.")
            time.sleep(10)
