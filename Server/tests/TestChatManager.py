import unittest
import ChatManager
import Room

class TestChatManager(unittest.TestCase):

	def test_parser(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "a","alias": "b","address": "c","room": "d","message": null}'
		self.assertEqual(cm.parse_incoming(jsin),{"command": "a","alias": "b","address": "c","room": "d","message": None})
	
	def test_execute_cmd(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "C","alias": "b","address": "c","room": "d","message": null}'
		cmd=cm.parse_incoming(jsin)
		self.assertEquals(cm.execute_cmd(cmd),0)
		
	def test_create_room(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd=cm.parse_incoming(jsin)
		self.assertEqual(cm.execute_cmd(cmd), 0)
		self.assertEqual(cm.get_room("RoomTest").get_name(),"RoomTest")

	def test_create_existing_room(self):
		cm = ChatManager.ChatManager()
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		self.assertEqual(cm.execute_cmd(cmd), "Room Exists")
		self.assertFalse(cm.execute_cmd(cmd))
	
	def test_join_room(self):
		cm = ChatManager.ChatManager()
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		self.assertEqual(cm.execute_cmd(cmd),0)
		self.assertEqual(cm.get_room("RoomTest").get_alias_list(),["Goh","Goh2"])

	def test_join_room_with_existing_alias(self):
		cm = ChatManager.ChatManager()
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		self.assertEqual(cm.execute_cmd(cmd),"User Exists")
		self.assertEqual(cm.get_room("RoomTest").get_alias_list(),["Goh",])


	def test_leave_room(self):
		cm = ChatManager.ChatManager()
		jsin = '{"command": "C","alias": "Goh","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		cm.execute_cmd(cmd)
		jsin = '{"command": "J","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		cm.execute_cmd(cmd)
		jsin = '{"command": "L","alias": "Goh2","address": "1234","room": "RoomTest","message": null}'
		cmd = cm.parse_incoming(jsin)
		self.assertEqual(cm.execute_cmd(cmd),0)
		self.assertEqual(cm.get_room("RoomTest").get_alias_list(),["Goh"])


if __name__=='__main__':
	unittest.main()