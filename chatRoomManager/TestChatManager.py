import unittest
import ChatManager

class TestChatManager(unittest.TestCase):

	def test_parser(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "a","alias": "b","address": "c","room": "d","message": null}'
		cm.parse_incoming(jsin)
	
	def test_execute_cmd(self):
		cm=ChatManager.ChatManager()
		jsin='{"command": "C","alias": "b","address": "c","room": "d","message": null}'
		cmd=cm.parse_incoming(jsin)
		cm.execute_cmd(cmd)

if __name__=='__main__':
	unittest.main()