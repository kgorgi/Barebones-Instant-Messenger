import threading
import queue
import socket
import time
import errno
from networking import Networking

class ServerNetwork(Networking):
    _host = socket.gethostname()
    _port = 8000

    def __init__(self):
        self._socket_dict = dict()

        self._rmsgs_queue = queue.Queue()
        self._smsgs_queue = queue.Queue()

        self._thread_lock = threading.Lock()

        accept_args = (self._socket_dict, self._thread_lock)
        self._accept_thread = threading.Thread(target = self._accept_sockets, args = accept_args )
        #self._accept_thread.setDaemon(True)
        self._accept_thread.start()


        rmsgs_args = (self._socket_dict, self._thread_lock, self._rmsgs_queue)
        self._rmsgs_thread = threading.Thread(target=self._exceute_receive, args=rmsgs_args)
        #self._rmsgs_thread.setDaemon(True)
        self._rmsgs_thread.start()

        smsgs_args = (self._socket_dict, self._thread_lock, self._smsgs_queue)
        self._smsgs_thread = threading.Thread(target=self._execute_send, args=smsgs_args)
        #self._smsgs_thread.setDaemon(True)
        self._smsgs_thread.start()


    def _accept_sockets(self, s_dict, d_lock):
        s = socket.socket()
        server_address = (self._host, self._port)
        s.bind(server_address)
        s.listen(5)

        while True:
            client, addr = s.accept()
            client.setblocking(0)
            str_addr = str(addr[0]) + ":" +  str(addr[1])

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
            else:
                time.sleep(1)

    def _exceute_receive(self, s_dict, d_lock, r_queue):
        while True:
            d_lock.acquire()
            for key, s in s_dict.items():
                try:
                    msg = s.recv(4096)
                    if len(msg) != 0:
                        self.__rmsgs_queue.put(msg.decode("utf-8"))
                except socket.error as e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        continue
                    else:
                        print("ERROR: " + str(e))
            d_lock.release()
            time.sleep(1)

    def send_response(self, address, response):
        e = {address, response}
        self._smsgs_queue.put(e)

    def send_message(self, addresses, msg):
        for adrs in addresses:
            e = (adrs, msg)
            self._smsgs_queue.put(e)

    def retrieve_next_message(self):
        if not self._rmsgs_queue.empty():
            return self._rmsgs_queue.get()
        return None


def main():
    n = ServerNetwork()

if __name__ == "__main__":
    main()