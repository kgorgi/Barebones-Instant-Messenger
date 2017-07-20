import time
import unittest
from chatmanager.chat_manager import ChatManager

class TestChatManager(unittest.TestCase):
    def setUp(self):
        self.cm = ChatManager()

    def tearDown(self):
        del self.cm

    def test_parser(self):
        jsin = '{"command": "a","alias": "b","address": "c","room": "d","message": null}'
        ans = {"command": "a","alias": "b","address": "c","room": "d","message": None}
        self.assertEqual(self.cm._parse_incoming(jsin), ans)


    def test__execute_invalid_cmd(self):
        cmd = self.create_command("D", "b", "c", "d", None)
        self.assertFalse(self.cm._execute_cmd(cmd))


    def test_create_room(self):
        cmd = self.create_command(None, "Goh", "1234", "RoomTest", None)
        self.cm.create_room(cmd)
        self.assertEqual(self.cm.get_room("RoomTest").get_name(),"RoomTest")

    def test_create_existing_room(self):
        cmd = self.create_command(None, "Goh", "address", "RoomTest", None)
        self.cm.create_room(cmd)
        self.assertFalse(self.cm.create_room(cmd))

    def test_join_room(self):
        cmd = self.create_command(None, "Goh", "1234", "RoomTest", None)
        self.cm.create_room(cmd)

        cmd2 = self.create_command(None, "Goh2", "12345", "RoomTest", None)
        self.cm.join_room(cmd2)

        self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh","Goh2"])
        self.assertEqual(self.cm.get_room("RoomTest").get_address_list(), ["1234", "12345"])

    def test_join_room_with_existing_alias(self):
        cmd = self.create_command(None, "Goh", "1234", "RoomTest", None)
        self.cm.create_room(cmd)

        cmd2 = self.create_command(None, "Goh", "1234", "RoomTest", None)

        self.assertEqual(self.cm.join_room(cmd2),1)
        self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh"])

    def test_leave_room(self):
        cmd = self.create_command("", "Goh", "1234", "RoomTest", "")
        self.cm.create_room(cmd)

        cmd2 = self.create_command("", "Goh2", "12345", "RoomTest", "")
        self.cm.join_room(cmd2)

        self.cm.leave_room(cmd2)

        self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh"])

    def create_command(self, command, alias, address, room, message):
        d = dict()

        if command is not None:
            d["command"] = command

        if alias is not None:
            d["alias"] = alias

        if address is not None:
            d["address"] = address

        if room is not None:
            d["room"] = room

        if message is not None:
            d["message"] = message

        return d

if __name__=='__main__':
    unittest.main()