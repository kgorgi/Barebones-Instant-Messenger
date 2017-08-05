import logging
import socket
import queue
import threading
import errno
import sys
from cnet.cnet_interface import Networking


class ClientNetworking(Networking):

    def __init__(self, address, port):
        self._successful_init = False
        logging.basicConfig(level=logging.INFO)
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
        self.is_connected = True

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
                else:
                    self.is_connected = False
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    self.is_connected = False
                    logging.debug("ERROR: " + str(e))
                    break

    def connected_to_server(self):
        return self.is_connected

    def shutdown(self):
        logging.info("ClientNetworking Shutting Down")
        if (self._successful_init):
            logging.info("Cleaning Up Socket")
            self.client_socket.close()
            logging.info("Successful Socket Cleanup")

    def __del__(self):
        self.shutdown()

