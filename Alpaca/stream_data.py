import config
import websocket, json

def on_open(ws):
    print("opened")
    auth_data = {"action": "auth", "key": "PKM83SCG7GK5OHPJKEEM", "secret": "EWs4qDxigKmPakY97ccqPdS3GPLhnxd8F017Hrid"}

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["T.Nqd;:!wrbn"]}}

    ws.send(json.dumps(listen_message))


def on_message(ws, message):
    print("received a message")
    print(message)

def on_close(ws):
    print("closed connection")

socket = "wss://paper-api.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()