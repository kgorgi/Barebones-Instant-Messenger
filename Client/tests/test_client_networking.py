import unittest
import socket
import threading
import time
from cnet.socket_client import ClientNetworking

class TestServerNetwork(unittest.TestCase):

    def setUp(self):
        self.server = socket.socket()
        self.server.bind(("127.0.0.1", 8000))
        self.server.listen(5)

    def tearDown(self):
        self.server.close()

    def test_connect_to_server(self):
        t = threading.Thread(target = self._start_client)
        t.start()
        addr, client = self.server.accept()
        self.client_socket = client
        time.sleep(5)

    def _start_client(self):
        c = ClientNetworking("127.0.0.1", 8000)
        time.sleep(2)
        c.shutdown()
        time.sleep(2)
        
    def test_send_message(self):
        t = threading.Thread(target=self._start_client_send)
        t.start()
        client, addr = self.server.accept()
        msg = client.recv(4096)
        self.assertEqual("1234TEST", msg.decode("utf-8"))
        time.sleep(5)

    def _start_client_send(self):
        c = ClientNetworking("127.0.0.1", 8000)
        msg = "1234TEST"
        c.send_message(msg)
        time.sleep(2)
        c.shutdown()
        time.sleep(2)


class TestServerNetworkReceive(unittest.TestCase):

    def setUp(self):
        t = threading.Thread(target=self._start_server)
        t.start()
        self.c = ClientNetworking("127.0.0.1", 8000)

    def tearDown(self):
        self.c.shutdown()
        time.sleep(3)

    def test_receive_message(self):
        msg = None
        while msg == None:
            msg = self.c.receive_next_message()
        self.assertEqual(msg, "TEST1456TEST" )

    def test_get_local_address(self):
        address = self.c.get_local_address()
        ans = socket.gethostname()
        if ".local" in ans:
            ans = "127.0.0.1"
        c_addr, port = address.split(":")
        self.assertEqual(c_addr, ans)

    def _start_server(self):
        server = socket.socket()
        server.bind(("127.0.0.1", 8000))
        server.listen(5)
        client, addr = server.accept()
        msg = "TEST1456TEST"
        client.send(msg.encode("utf-8"))
        server.close()

if __name__ == '__main__':
    unittest.main()