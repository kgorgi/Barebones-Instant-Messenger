import threading
import queue
import socket
import time
import errno
import atexit
import logging
from snet.snet_interface import Networking

class ServerNetwork(Networking):


    def __init__(self, address, port):
        logging.basicConfig(level=logging.INFO)
        logging.info("Starting Server Networking")

        self._host = address
        self._port = port


        self._socket_dict = dict()
        self._accept_s = socket.socket()

        self._rmsgs_queue = queue.Queue()
        self._smsgs_queue = queue.Queue()

        self._thread_lock = threading.Lock()

        logging.info("Creating Accept Socket Thread")
        accept_args = (self._accept_s, self._socket_dict, self._thread_lock)
        self._accept_thread = threading.Thread(target = self._accept_sockets, args = accept_args )
        self._accept_thread.setDaemon(True)
        self._accept_thread.start()

        logging.info("Creating Receive Messages Thread")
        rmsgs_args = (self._socket_dict, self._thread_lock, self._rmsgs_queue)
        self._rmsgs_thread = threading.Thread(target=self._exceute_receive, args=rmsgs_args)
        self._rmsgs_thread.setDaemon(True)
        self._rmsgs_thread.start()

        logging.info("Creating Send Messages Thread")
        smsgs_args = (self._socket_dict, self._thread_lock, self._smsgs_queue)
        self._smsgs_thread = threading.Thread(target=self._execute_send, args=smsgs_args)
        self._smsgs_thread.setDaemon(True)
        self._smsgs_thread.start()

        atexit.register(self.__del__)

    def _accept_sockets(self,s, s_dict, d_lock):
        server_address = (self._host, self._port)
        logging.info("Binding To: " + str(server_address))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(server_address)

        s.listen(5)

        while True:
            try:
                client, addr = s.accept()
            except ConnectionAbortedError:
                logging.debug("Accept Socket: Connection Aborted")
                return
            except OSError as e:
                logging.debug("Accept Socket: OS Error")
            client.setblocking(0)
            str_addr = str(addr[0]) + ":" +  str(addr[1])
            logging.info("Adding Client: " + str_addr)
            d_lock.acquire()
            s_dict[str_addr] = client
            d_lock.release()

    def _execute_send(self, s_dict, d_lock, s_queue):
        while True:
            if not s_queue.empty():
                addr, msg_to_send = s_queue.get()
                s_queue.task_done()
                d_lock.acquire()
                s_dict[addr].send(msg_to_send.encode("utf-8"))
                d_lock.release()
                logging.info("Sent(" + addr + "): " + msg_to_send)
            else:
                time.sleep(1)

    def _exceute_receive(self, s_dict, d_lock, r_queue):
        while True:
            d_lock.acquire()
            for key, s in s_dict.items():
                try:
                    msg = s.recv(4096)
                    if len(msg) != 0:
                        msg = msg.decode("utf-8")
                        logging.info("Received(" + key + "): " + msg)
                        self._rmsgs_queue.put(msg)
                except socket.error as e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        continue
                    else:
                        logging.debug(str(e))
            d_lock.release()
            time.sleep(1)

    def send_response(self, address, response):
        e = (address, response)
        self._smsgs_queue.put(e)

    def send_message(self, addresses, msg):
        for adrs in addresses:
            e = (adrs, msg)
            self._smsgs_queue.put(e)

    def retrieve_next_message(self):
        if not self._rmsgs_queue.empty():
            return self._rmsgs_queue.get()
        return None

    def _socket_cleanup(self):
        logging.info("Cleaning Up Sockets")
        self._thread_lock.acquire()
        for key, s in self._socket_dict.items():
            try:
                s.shutdown(socket.SHUT_RDWR)
            except:
                logging.info("Socket(" + key + "): Not Connected ")
        logging.info("Successful Socket Cleanup")
        self._accept_s.close()
        self._thread_lock.release()

    def shutdown(self):
        self._socket_cleanup()

    def __del__(self):
        self.shutdown()

def main():
    n = ServerNetwork("127.0.0.1", 8000)
    input("Press a key to exit\n")

if __name__ == "__main__":
    main()