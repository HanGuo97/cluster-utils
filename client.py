import zmq
import time

SERVER = "nlp5.cs.unc.edu:5560"
TOPIC_FILTER = b"SERVER"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://%s" % SERVER)
socket.setsockopt(zmq.SUBSCRIBE, TOPIC_FILTER)
print("Connected to server %s" % SERVER)


def client():
    while True:
        message = socket.recv()
        print(message.decode())
        time.sleep(1)


if __name__ == "__main__":
    client()
