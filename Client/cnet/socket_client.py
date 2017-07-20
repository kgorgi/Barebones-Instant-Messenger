import logging
import socket
import queue
import threading
import time
import errno
import sys
from cnet.cnet_interface import Networking


class ClientNetworking(Networking):

    def __init__(self, address, port):
        self._successful_init = False
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Starting Client Networking")

        self._host = address
        self._port = port

        self.send_msg_queue = queue.Queue()
        self.received_msg_queue = queue.Queue()

        address = (self._host, self._port)
        logging.info("Attempting to Connect to: " + self._host + ":" + str(self._port))
        self.client_socket = socket.socket()
        try:
            self.client_socket.connect(address)
        except ConnectionRefusedError as e:
            logging.debug("Connection Failed: Connection Refused")
            sys.exit(0)
        except Exception as e:
            logging.debug("Connection Failed")
            sys.exit(0)

        logging.info("Successfully Connected")

        args_send = (self.client_socket ,self.send_msg_queue)
        self.send_msg_thread = threading.Thread(target=self.execute_send, args= args_send)
        self.send_msg_thread.setDaemon(True)
        self.send_msg_thread.start()

        args_receive = (self.client_socket, self.received_msg_queue)
        self.receive_msg_thread = threading.Thread(target=self.execute_receive, args=args_receive)
        self.receive_msg_thread.setDaemon(True)
        self.receive_msg_thread.start()

        self._successful_init = True

    def get_local_address(self):
        addr, port = (self.client_socket.getsockname())
        return "" + addr + ":" + str(port)

    def send_message(self, msg):
        self.send_msg_queue.put(msg)

    def execute_send(self, s ,s_queue):
        while True:
            msg_to_send = s_queue.get()
            s_queue.task_done()
            logging.info("Sending message: " + "\"" + msg_to_send.rstrip(" ")+  "\"")

            s.send(msg_to_send.encode('utf-8'))

    def receive_next_message(self):
        if not self.received_msg_queue.empty():
            return self.received_msg_queue.get()
        return None

    def execute_receive(self, s , r_queue):
        while True:
            try:
                msg_received = s.recv(280)
                if len(msg_received) != 0:
                    msg_received = msg_received.decode("utf-8").rstrip(" ")
                    r_queue.put(msg_received)
                    logging.info("Received Message: " + "\"" +  msg_received + "\"")
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    logging.debug("ERROR: " + str(e))
                    break

    def shutdown(self):
        logging.info("ClientNetworking Shutting Down")
        if (self._successful_init):
            logging.info("Cleaning Up Socket")
            self.client_socket.close()
            logging.info("Successful Socket Cleanup")

    def __del__(self):
        self.shutdown()


def main():
    i = ClientNetworking("127.0.0.1", 8000)
    i.send_message("hello spicy boy")

    time.sleep(5)
    i.shutdown()
    """""
    clients = list()
    for i in range(1, 200):
        print(str(i))
        temp = ClientNetworking()
        clients.append(temp)

    print("Connection Created!")
    x = 0;
    for c in clients:
        x += 1
        c.send_message(str(x))

    time.sleep(10)
    print("SENT!")
    while True:
        for c in clients:
            msg = c.receive_next_message()
            if msg != None:
                print("recieved:"+msg)

    time.sleep(10)


    """


if __name__ == "__main__":
    main()


