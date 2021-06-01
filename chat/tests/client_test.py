import websocket
import time
import json
import _thread

def on_message(ws, message):
    pass
    #print ('message : ', message)

def on_error(ws, error):
    print ("eroror:", error)

def on_close(ws):
    print ("### closed ###")
    # Attemp to reconnect with 2 seconds interval
    time.sleep(2)
    initiate()

def on_open(ws):
    user = input("input your name : ")
    print ("### Initiating new websocket connectipython my-websocket.pyon ###")
    def run(*args):
        for i in range(30000):
            # Sending message with 1 second intervall
            time.sleep(1)
            message = input("input your message : ")
            ws.send(json.dumps({'message': message, 'type':'chat.message', 'user':user}))
        time.sleep(1)
        ws.close()
        print ("thread terminating...")
    _thread.start_new_thread(run, ())

def initiate():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/api/chat/test/",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()

if __name__ == "__main__":
    initiate()
