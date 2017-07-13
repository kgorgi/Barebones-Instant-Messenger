import unittest
import socket
import queue
import socket
from snet.socket_server import ServerNetwork


class TestServerNetwork(unittest.TestCase):
    def setUp(self):
        self.server_N = ServerNetwork()
        self.client_s = socket.socket()

    def tearDown(self):
        del self.server_N
        self.client_s.close()

    def test_add_client(self):
        address = (socket.gethostname(), 8000)
        try:
            self.client_s.connect(address)
        except ConnectionRefusedError:
            self.fail("Cannot Connect to Server")

    def test_send_message(self):
        pass

    def test_receive_message(self):
        pass


if __name__ == '__main__':
    unittest.main()