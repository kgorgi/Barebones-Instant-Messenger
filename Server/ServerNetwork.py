import sys
from Networking import Networking
import threading
import queue
import socket
import time
import errno

class ServerNetwork(Networking):
    __host = socket.gethostname()
    __port = 8000

    def __init__(self):
        self.__socket_dict = dict()

        self.__rmsgs_queue = queue.Queue()
        self.__smsgs_queue = queue.Queue()

        self.__thread_lock = threading.Lock()

        accept_args = (self.__socket_dict, self.__thread_lock)
        self.__accept_thread = threading.Thread(target = self.__accept_sockets, args = accept_args )
        #self.__accept_thread.setDaemon(True)
        self.__accept_thread.start()


        rmsgs_args = (self.__socket_dict, self.__thread_lock, self.__rmsgs_queue)
        self.__rmsgs_thread = threading.Thread(target=self.__exceute_receive, args=rmsgs_args)
        #self.__rmsgs_thread.setDaemon(True)
        self.__rmsgs_thread.start()

        smsgs_args = (self.__socket_dict, self.__thread_lock, self.__smsgs_queue)
        self.__smsgs_thread = threading.Thread(target=self.__execute_send, args=smsgs_args)
        #self.__smsgs_thread.setDaemon(True)
        self.__smsgs_thread.start()


    def __accept_sockets(self, s_dict, d_lock):
        s = socket.socket()
        server_address = (self.__host, self.__port)
        s.bind(server_address)
        s.listen(5)

        while True:
            client, addr = s.accept()
            client.setblocking(0)
            str_addr = str(addr[0]) + ":" +  str(addr[1])

            d_lock.acquire()
            s_dict[str_addr] = client
            d_lock.release()

    def __execute_send(self, s_dict, d_lock, s_queue):
        while True:
            if not s_queue.empty():
                addr, msg_to_send = s_queue.get()
                s_queue.task_done()
                d_lock.acquire()
                s_dict[addr].send(msg_to_send.encode("utf-8"))
                d_lock.release()
            else:
                time.sleep(1)

    def __exceute_receive(self, s_dict, d_lock, r_queue):
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

    def send_error(self, address, error):
        e = {address, error}
        self.__smsgs_queue.put(e)

    def send_message(self, addresses, msg):
        for adrs in addresses:
            e = (adrs, msg)
            self.__smsgs_queue.put(e)

    def retrieve_next_message(self):
        if not self.__rmsgs_queue.empty():
            return self.__rmsgs_queue.get()
        return None

def main():
    n = ServerNetwork()

if __name__ == "__main__":
    main()