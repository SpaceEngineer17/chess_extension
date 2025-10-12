import engine
from websocket_server import WebsocketServer
import sys
import time
import threading
import logging


CERT = "fullpath ./_cert.pem"
KEY  = "fullpath ./_key"
PASS = "password" # <-- password for ./_key is "password"

HOST = "127.0.0.1"
PORT = 9999


fish = engine.Engine("/usr/local/games/stockfish")
print(fish.setEngineParameters({"Threads" : 16, "Hash" : 256, "UCI_Elo": 3190}))

def ping(server: WebsocketServer, client):
  while True:
    time.sleep(10)
    try:
      server.send_message(client, "ping")
    except:
      log("Exiting Client ", client['id'])
      return

def parse_message(message: str):
  if "Move:" in message:
    mv = message.split("Move: ")[1]
    print(" ".join(fish.moves[0]) + " " + mv)
    fish.addMove(mv)
    fish.setPosition()
    best_move = fish.go("movetime 5000")[-1].split(" ")[1]
    print("Best Move: ", best_move)
    return "BestMove: " + best_move
  elif "ResetGame: " in message:
    #gameid = int(message.split("ResetGame: ")[1])
    fish.resetMoves()

  else:
    return None

def log(*str):
  print(*str, file=sys.stderr) # sys.stderr = sys.stdout

def onconnect(client, server: WebsocketServer):
  log("Client Connected: %d" % client['id'])
  server.send_message_to_all("ALERT ALL SYSTEMS: A new Client(%d) has connected" % client['id'])
  threading.Thread(name="Thread%d" % client['id'], target=ping, args=[server, client]).start()

def onclose(client, server: WebsocketServer):
  log("Cliend Disconnected: %d" % client['id'])
  server.send_message_to_all("ALERT ALL SYSTEMS: A new Client(%d) has dis-connected" % client['id'])

def onmessage(client, server:WebsocketServer, message):
  if message=="pong":
    return
  log("Client %d:" % client['id'], message)
  ret = parse_message(message)
  if ret!=None:
    server.send_message(client, ret)


wss = WebsocketServer(host=HOST, port = PORT, cert=CERT, key=KEY, password=PASS, loglevel=logging.INFO)
# wss = WebsocketServer(host=HOST, port = PORT, loglevel=logging.INFO)
wss.set_fn_new_client(onconnect)
wss.set_fn_client_left(onclose)
wss.set_fn_message_received(onmessage)
wss.run_forever()
