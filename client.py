import zmq
import time
from datetime import datetime
from constants import (FORWARDER_URL,
                       BACKEND_PORT,
                       TOPIC_FILTER)


# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://%s:%s" % (FORWARDER_URL, BACKEND_PORT))
socket.setsockopt(zmq.SUBSCRIBE, TOPIC_FILTER)
print("Connected to server %s:%s" % (FORWARDER_URL, BACKEND_PORT))


def _process_message(message):
    msg_lines = message.splitlines()
    host_name = msg_lines[0].split()[1]
    gpu_mem = [
        l[1:-1].split("|")[-1].strip()[:-1]
        for l in msg_lines[3:]]

    gpu_info = " ".join(gpu_mem)
    time_info = str(datetime.now().time())
    return host_name, gpu_info, time_info


def _print_gpu_info(status):
    for key, val in status.items():
        print("\033[95m %s \033[0m \n %s" % (key, val))
    print("\n\n\n")


def client():
    gpu_status = {}
    while True:
        message = socket.recv().decode()
        host_name, gpu_info, time_info = _process_message(message)

        gpu_status[host_name] = "MEM:\t%s \nTIME:\t%s" % (gpu_info, time_info)
        _print_gpu_info(gpu_status)
        time.sleep(3)


if __name__ == "__main__":
    client()
