import zmq
import time
from constants import (FORWARDER_URL,
                       BACKEND_PORT,
                       TOPIC_FILTER)


# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://%s:%s" % (FORWARDER_URL, BACKEND_PORT))
socket.setsockopt(zmq.SUBSCRIBE, TOPIC_FILTER)
print("Connected to server %s" % FORWARDER_URL)


def client():
    while True:
        message = socket.recv()
        print(message.decode())
        time.sleep(1)


if __name__ == "__main__":
    client()
