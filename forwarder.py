import zmq
from constants import FRONTEND_PORT, BACKEND_PORT


def main():
    """https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/forwarder.html"""
    try:
        # Initialize the Context
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:%s" % FRONTEND_PORT)

        # Set the Socket Opt
        frontend.setsockopt(zmq.SUBSCRIBE, b"")

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:%d" % BACKEND_PORT)
        print("Forwarder binded to %s %s" % (FRONTEND_PORT, BACKEND_PORT))

        # Start the device
        zmq.device(zmq.FORWARDER, frontend, backend)
    
    except Exception as e:
        print(e)
        print("bringing down zmq device")
    
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


if __name__ == "__main__":
    main()
