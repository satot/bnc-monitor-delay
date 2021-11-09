# https://github.com/binance/binance-spot-api-docs/blob/master/user-data-stream.md#general-wss-information
import websocket
import _thread
from time import time
import json

def get_delay():
    while True:
        try:
            delay = int(input("Delay time (ms): "))
            if 0 <= delay <= 50000:
                return delay
            else:
                print("The delay must be in 0-50000")
        except ValueError:
            print("Please enter integer")

def get_listen_key():
    while True:
        lk = str(input("listen key: "))
        if len(lk) == 60:
            return lk
        else:
            print("Invalid listen key")

class WsMonitor:
    ws_server_host = "wss://testnet.binance.vision/ws/"

    # listen_key: Need to be generated from POST /api/v3/userDataStream API
    # delay: Alert when delay exceed this amount (ms)
    def __init__(self, listen_key, delay, is_debug=False):
        self.ws_server_host += listen_key
        self.delay = delay
        self.is_debug = is_debug

    def log(self, message):
        if self.is_debug:
            print(message, flush=True)

    def start(self):
        if self.is_debug:
            websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
                self.ws_server_host,
                on_open=self.on_open,
                on_ping=self.on_ping,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
        ws.run_forever()

    def is_delayed(self, eventTime):
        return abs(time() * 1000 - eventTime) >= self.delay

    def on_message(self, ws, message):
        self.log("### message received ###: " + message)
        try:
            m = json.loads(message)
            if "e" not in m.keys() or m["e"] != "executionReport":
                return
            self.log("currentTime: {0}, eventTime: {1}".format(time() * 1000, m["E"]))
            if "E" in m.keys() and self.is_delayed(m["E"]):
                print("Message has delayed!", flush=True)
        except ValueError:
            self.log(message, flush=True)

    def on_error(self, ws, error):
        self.log("### error received ###: " + error)

    def on_close(self, ws, close_status_code, close_msg):
        self.log("### closed ###")

    def on_ping(self, ws, message):
        self.log("### ping received ###: " + message)

    def on_open(self, ws):
        def run(*args):
            init_msg = {
                "method": "SUBSCRIBE",
                "topic": "orders",
                "params": ["address"],
                "id": 12345
            }
            ws.send(json.dumps(init_msg))
        _thread.start_new_thread(run, ())

if __name__ == "__main__":
    delay = get_delay()
    lk = get_listen_key()
    WsMonitor(lk ,delay, True).start()

