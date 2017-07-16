import unittest
import socket
from snet.socket_server import ServerNetwork


class TestServerNetwork(unittest.TestCase):
    def setUp(self):
        self.server_N = ServerNetwork()
        self.client_s = socket.socket()

    def tearDown(self):
        self.server_N.shutdown()
        self.client_s.close()

    def test_add_client(self):
        address = ("127.0.0.1", 8000)
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