from Networking import Networking
import threading
import queue
import socket
import time

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

        self.__smsgs_thread = None
        self.__rmsgs_thread = None
        self.__accept_thread.start()


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
        pass

    def __excute_recieve(self, s_dict, d_lock, r_queue):
        pass

    def send_error(self, address, error):
        e = {address, error}
        self.__smsgs_queue.put(e)

    def send_message(self, addresses, msg):
        for adrs in addresses:
            e = {adrs, msg}
            self.__smsgs_queue.put(e)

    def retrieve_next_message(self):
        if not self.__rmsgs_queue.empty():
            return self.rmsgs_queue.get()
        return None

def main():
    n = ServerNetwork()

if __name__ == "__main__":
    main()

