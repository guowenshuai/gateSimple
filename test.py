#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
# 所有交易名称
https://data.gateapi.io/api2/1/pairs
'''
import websocket
from influxdb import InfluxDBClient
# ws = create_connection("wss://ws.gate.io/v3/")
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"id":1010110, "method":"ticker.subscribe", "params":["ETH_USDT"]}')    
    # thread.start_new_thread(run, ())


def on_message(ws, message):
    message =  json.loads(message)
    print(message)
    try:
        name = message['params'][0]
        fields =  message['params'][1]
        for k, v in fields.items():
            fields[k] = float(v)
        body = [{
            "measurement": "ticker",
            "tags": {
                "name": name
            },
            "fields": fields
        }]
        client.write_points(body)
    except Exception as e:
        print("err: ", str(e))




# 初始化（指定要操作的数据库）
client = InfluxDBClient(host='localhost', port=8086, database="gateio")

# print(client.get_list_measurements())

# {"method": "ticker.update", "params": ["ETH_USDT", {"period": 86400, "open": "590.88", "close": "589.03", "high": "596.81", "low": "561", "last": "589.03", "change": "-0.12", "quoteVolume": "40939.1832124219", "baseVolume": "23801126.67374223112472126573"}], "id": null}


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.gateio.ws/v4/",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

  
