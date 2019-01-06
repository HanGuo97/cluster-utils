import sys
import zmq
import time
import GPUtil
# from StringIO import StringIO  # Python2
from io import StringIO  # Python3

FORWARDER_URL = "nlp5.cs.unc.edu:5559"


# Setup the Connection
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://%s" % FORWARDER_URL)
print("Server Binded to %s" % FORWARDER_URL)



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


def _get_publisher_name():
    return "Random1"


def server():
    publisher_name = _get_publisher_name()
    while True:
        #  Do some 'work'
        response = process()
        response = "SERVER #%s \n %s" % (publisher_name, response)
        print("Sending Response\n%s" % response)
        #  Send reply back to client
        socket.send(response.encode())
        time.sleep(1)


if __name__ == "__main__":
    server()
