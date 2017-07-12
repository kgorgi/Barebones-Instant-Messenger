from Client.Networking import Networking
import logging
import json
import socket
import queue
import threading
from threading import Thread
import time


class ClientNetworking(Networking):
    __host = "134.87.139.78"
    __port = 8000

    def __init__(self):

        self.send_msg_queue = queue.Queue()
        self.received_msg_queue = queue.Queue()

        address = (self.__host, self.__port)
        self.client_socket = socket.socket()
        self.client_socket.connect(address)

        args_send = (self.client_socket, self.send_msg_queue)
        self.send_msg_thread = threading.Thread(target=self.execute_send, args= args_send)
        #self.send_msg_thread.setDaemon(True)
        self.send_msg_thread.start()

        args_receive = (self.client_socket, self.received_msg_queue)
        self.receive_msg_thread = threading.Thread(target=self.execute_receive, args=args_receive)
        #self.receive_msg_thread.setDaemon(True)
        self.receive_msg_thread.start()

        #self.thread_lock = threading.lock()



    def send_message(self, msg):
        self.send_msg_queue.put(msg)

    def retrieve_next_message(self):
        if not self.received_msg_queue.empty():
            return self.received_msg_queue.get()



    def execute_send(self, socket, s_queue):
        while True:
            if not s_queue.empty():
                msg_to_send = s_queue.get()
                s_queue.task_done()
                print("Sending message:" + msg_to_send)
                logging.debug("Sending a message from the queue")
                socket.send(msg_to_send.encode('utf-8'))
            else:
                print("No messages to send sir/madame")
            time.sleep(1)

    def execute_receive(self, socket, r_queue):
        while True:
            #try:
                #(serverSocket, address) = self.client_socket.accept()
            pass





def main():
    i = ClientNetworking()

    i.send_message("hello spicy boy")

    p = ClientNetworking()

    p.send_message("hello spicy boi")

    for i in range(1,10):
        temp = ClientNetworking()
        temp.send_message(str(i))
        print(str(i))

    time.sleep(10)

if __name__ == "__main__":
    main()


