import unittest
import socket
import threading
import time
from cnet.socket_client import ClientNetworking
from clienthandler.client_handler import ClientHandler


class TestServerNetwork(unittest.TestCase):

    def test_create(self):
        handler = ClientHandler()
        self.assertEqual(str(handler.create_room("test_room_1", "test_alias")), '0')
        self.assertEqual(str(handler.create_room("test_room_1", "test_alias")), '2')
        handler.leave_room()

    def test_join(self):
        handler = ClientHandler()
        handler2 = ClientHandler()
        handler.create_room("test_room_1", "test_alias_1")
        self.assertEqual(str(handler2.join_room("test_room_1", "test_alias_2")), '0')
        handler2.leave_room()
        handler.leave_room()



if __name__ == '__main__':
    unittest.main()