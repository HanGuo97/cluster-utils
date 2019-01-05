import zmq

context = zmq.Context()
SERVER = "bvisionserver6.cs.unc.edu:5555"

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://%s" % SERVER)
print("Connected to server %s…" % SERVER)


def client():
    print("Sending request …")
    socket.send(b"GPU-STATUS")

    #  Get the reply.
    message = socket.recv()
    print("Received reply")
    print(message.decode())


if __name__ == "__main__":
    client()
