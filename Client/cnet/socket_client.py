import logging
import socket
import queue
import threading
from threading import Thread
import time
import errno
from cnet.cnet_interface import Networking


class ClientNetworking(Networking):
    __host = "127.0.0.1"
    __port = 8000

    def __init__(self):

        self.send_msg_queue = queue.Queue()
        self.received_msg_queue = queue.Queue()

        address = (self.__host, self.__port)
        print("Attempting to connect!")
        self.client_socket = socket.socket()
        self.client_socket.connect(address)
        self.client_socket.setblocking(0)
        print("connected")

        self.thread_lock = threading.Lock()

        args_send = (self.client_socket, self.thread_lock ,self.send_msg_queue)
        self.send_msg_thread = threading.Thread(target=self.execute_send, args= args_send)
        #self.send_msg_thread.setDaemon(True)
        self.send_msg_thread.start()

        args_receive = (self.client_socket, self.thread_lock, self.received_msg_queue)
        self.receive_msg_thread = threading.Thread(target=self.execute_receive, args=args_receive)
        #self.receive_msg_thread.setDaemon(True)
        self.receive_msg_thread.start()

    def get_local_address(self):
        addr, port = (self.client_socket.getsockname())
        return "" + addr + ":" + str(port)

    def send_message(self, msg):
        self.send_msg_queue.put(msg)

    def execute_send(self, s, lock_s ,s_queue):
        while True:
            if not s_queue.empty():
                msg_to_send = s_queue.get()
                s_queue.task_done()
                print("Sending message: " + "\"" + msg_to_send+ "\"")
                lock_s.acquire()
                s.send(msg_to_send.encode('utf-8'))
                lock_s.release()
            else:
                pass
                #Wait a bit before you check again
                time.sleep(0.05)

    def receive_next_message(self):
        if not self.received_msg_queue.empty():
            return self.received_msg_queue.get()
        return None

    def execute_receive(self, s, lock_r , r_queue):
        while True:

            try:
                msg_received = s.recv(4096)
                if len(msg_received) != 0:
                    msg_received = msg_received.decode("utf-8")
                    r_queue.put(msg_received)
                    print("Received Message: " + "\"" +  msg_received + "\"")
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    continue
                else:
                    print("ERROR: " + str(e))

            time.sleep(1)




def main():
    i = ClientNetworking()
    i.send_message("hello spicy boy")

    print(i.get_local_address())
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


