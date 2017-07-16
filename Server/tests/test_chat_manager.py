import time
import unittest
from chatmanager.chat_manager import ChatManager
from chatmanager.room import Room

class TestChatManager(unittest.TestCase):
	def setUp(self):
		self.cm = ChatManager()

	def tearDown(self):
		del self.cm

	def test_parser(self):
		jsin='{"command": "a","alias": "b","address": "c","room": "d","message": null}'
		self.assertEqual(self.cm.parse_incoming(jsin),{"command": "a","alias": "b","address": "c","room": "d","message": None})

	def test_execute_cmd(self):
		jsin='{"command": "C","alias": "b","address": "c","room": "d","message": null}'
		cmd=self.cm.parse_incoming(jsin)
		self.assertEquals(self.cm.execute_cmd(cmd),0)
		
	def test_create_room(self):
		jsin='{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd=self.cm.parse_incoming(jsin)
		self.assertEqual(self.cm.execute_cmd(cmd), 0)
		self.assertEqual(self.cm.get_room("RoomTest").get_name(),"RoomTest")

	def test_create_existing_room(self):
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.assertFalse(self.cm.execute_cmd(cmd))

	def test_join_room(self):
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.assertEqual(self.cm.execute_cmd(cmd),True)
		self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh","Goh2"])

	def test_join_room_with_existing_alias(self):
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.assertFalse(self.cm.execute_cmd(cmd),"User Exists")
		self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh",])

	def test_leave_room(self):
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.cm.execute_cmd(cmd)
		jsin = '{"command": "L","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = self.cm.parse_incoming(jsin)
		self.assertEqual(self.cm.execute_cmd(cmd),True)
		self.assertEqual(self.cm.get_room("RoomTest").get_alias_list(),["Goh"])

if __name__=='__main__':
	unittest.main()