import os
import threading
import fcntl
import time


#Creating pipes
r, w = os.pipe()

stdin = os.fdopen(w, "wb", buffering=0)
stdout = os.fdopen(r, "rb", buffering=0)

#Make stdout non-blocking
flags = fcntl.fcntl(r, fcntl.F_GETFL)
fcntl.fcntl(r, fcntl.F_SETFL, flags | os.O_NONBLOCK)

#Simulating input
def inp():
  c = 0
  while c<100:
    stdin.write(("Hi %d" %c).encode()) #<-- ERROR After timed out in non-blocking pipe
    #stdin.flush() #no need as bufzise = 0
    c += 1
    time.sleep(1)

def get():
    while True:
      try:
        buff = stdout.read(1)
        if buff == None:
          print("--Timeout")
          break
        print(buff.decode(), end="")
      except ValueError:
        pass


#Sending input from other thread to make time for output reading on main thread
th = threading.Thread(target = inp, args=[])
th.start()

#Reading output with non-blocking pipe mode
get()

stdin.close()
stdout.close()

## CONCLUSION ## ##NOT SUITABLE FOR READING ENGINE OUTPUT##
# cuz we need timeout & always OPENed pipes
"""
Once a READ operation on NON-Blocking PIPE is TIMED OUT, 
the InputStream is closed (EOF)
and we cannot WRITE to InputStream and
cannot READ from OutputStream (cuz no input)
"""

