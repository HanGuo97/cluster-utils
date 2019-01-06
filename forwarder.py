import zmq
FRONTEND_PORT = 5559
BACKEND_PORT = 5560


def main():

    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:%s" % FRONTEND_PORT)

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
