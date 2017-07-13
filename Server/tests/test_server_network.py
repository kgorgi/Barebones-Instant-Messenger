import unittest
import socket
import queue
import socket
from networking.server_networking import ServerNetwork


class TestRoom(unittest.TestCase):
    def setUp(self):
        self.server_N = ServerNetwork()
        self.client_s = socket.socket()


    def tearDown(self):
        address = (socket.gethostname(), 8000)
        try:
            self.client_s.connect(address)
        except ConnectionRefusedError:
            self.fail("Cannot Connect to Server")


    def test_add_client(self):
        pass

    def test_send_message(self):
        pass

    def test_receive_message(self):
        pass


if __name__ == '__main__':
    unittest.main()