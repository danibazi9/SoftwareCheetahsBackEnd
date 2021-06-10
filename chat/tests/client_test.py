import websocket
import time
import json
import _thread

def on_message(ws, message):
    print ('message : ', message)

def on_error(ws, error):
    print ("eroror:", error)

def on_close(ws):
    print ("### closed ###")
    # Attemp to reconnect with 2 seconds interval
    time.sleep(2)
    initiate()

def on_open(ws):
    #token = input("input your token : ")
    token = '8a492f3aef1f8abfaad5222a4f56a118ea1ca271'
    ws.send(json.dumps({'type':'authenticate', 'Authorization': token}))
    print ("### Initiating new websocket connectipython my-websocket.pyon ###")
    def run(*args):
        for i in range(30000):
            # Sending message with 1 second intervall
            time.sleep(1)
            message = input("input your message : ")
            #ws.send(json.dumps({'message': message, 'type':'create'}))
            #ws.send(json.dumps({'message_id': int(message), 'type':'delete'}))
            ws.send(json.dumps({'message_id': 11, 'type':'update', 'text':message}))
            ws.send(json.dumps({'type':'fetch'}))
        time.sleep(1)
        ws.close()
        print ("thread terminating...")
    _thread.start_new_thread(run, ())

def initiate():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/api/chat/1/",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()

if __name__ == "__main__":
    initiate()