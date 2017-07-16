import unittest
import socket
import time
from snet.socket_server import ServerNetwork


class TestServerNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_N = ServerNetwork("127.0.0.1", 8000)
        cls.client_s = socket.socket()

    @classmethod
    def tearDownClass(cls):
        cls.server_N.shutdown()
        cls.client_s.close()

    def test_add_client(cls):
        address = ("127.0.0.1", 8000)
        try:
            cls.client_s.connect(address)
        except ConnectionRefusedError:
            cls.fail("Cannot Connect to Server")

    def test_receive_message(cls):
        msg = "Testing12345"
        cls.client_s.send(msg.encode("utf-8"))
        time.sleep(2)
        cls.assertEqual(cls.server_N.retrieve_next_message(),msg)


    def test_send_response(cls):
        msg = "TESTING54321"
        addr, port = (cls.client_s.getsockname())
        address = "127.0.0.1:" + str(port)
        cls.server_N.send_response(address, msg)
        client_msg = cls.client_s.recv(4096)
        cls.assertEqual(msg, client_msg.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()