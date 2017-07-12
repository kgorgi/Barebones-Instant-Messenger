import unittest
import ChatManager

class TestChatManager(unittest.TestCase):

	def test_parser(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "a","alias": "b","address": "c","room": "d","message": null}'
		self.assertEqual(cm.parse_incoming(jsin),{"command": "a","alias": "b","address": "c","room": "d","message": None})
	
	def test_execute_cmd(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "C","alias": "b","address": "c","room": "d","message": null}'
		cmd=cm.parse_incoming(jsin)
		self.assertTrue(cm.execute_cmd(cmd))
		
	#def test_create_room(self):
	
	#def test_create_existing_room(self):
	
	#def test_join_room
	
	#def test_leave_room
	
	#def test_send_message

if __name__=='__main__':
	unittest.main()