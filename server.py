import sys
import zmq
import time
import GPUtil
# from StringIO import StringIO  # Python2
from io import StringIO  # Python3
import socket as socket_utils
from constants import FORWARDER_URL, FRONTEND_PORT


# Setup the Connection
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://%s:%s" % (FORWARDER_URL, FRONTEND_PORT))
print("Server Binded to %s:%s" % (FORWARDER_URL, FRONTEND_PORT))


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


# IP address
def get_Host_name_IP():
    try:
        host_name = socket_utils.gethostname()
        host_ip = socket_utils.gethostbyname(host_name)
        # print("Hostname : ", host_name)
        # print("IP : ", host_ip)
        return "%s %s" % (host_name, host_ip)
    except Exception:
        print("Unable to get Hostname and IP")


def server():
    publisher = get_Host_name_IP()
    while True:
        #  Do some 'work'
        response = process()
        response = "SERVER %s \n %s" % (publisher, response)
        # print("Sending Response\n%s" % response)
        
        #  Send reply back to client
        socket.send(response.encode())
        time.sleep(1)


if __name__ == "__main__":
    server()
