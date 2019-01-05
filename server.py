import sys
import zmq
import GPUtil
# from StringIO import StringIO  # Python2
from io import StringIO  # Python3

PORT = 5555

# Setup the Connection
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%d" % PORT)
print("Server Binded to %d" % PORT)


def _get_GPU_status():
    GPUtil.showUtilization()


def process():
    # https://wrongsideofmemphis.com/2010/03/01/store-standard-output-on-a-variable-in-python/

    # Store the reference in case you want
    # to show things again in standard output
    old_stdout = sys.stdout

    # This variable will store everything that is
    # sent to the standard output
    result = StringIO()
    sys.stdout = result

    # Here we can call anything we like, like external
    # modules, and everything that they will send to standard
    # output will be stored on "result"
    _get_GPU_status()

    # Redirect again the std output to screen
    sys.stdout = old_stdout

    # Then, get the stdout like a string and process it!
    result_string = result.getvalue()

    return result_string


def server():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        response = process()

        #  Send reply back to client
        socket.send(response.encode())


if __name__ == "__main__":
    server()
