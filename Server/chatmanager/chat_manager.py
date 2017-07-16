import json
import logging
from chatmanager.room import Room
from snet.socket_server import ServerNetwork

class ChatManager:
	_host = "127.0.0.1"
	_port = 8000

	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		logging.info("Starting ChatManager")
		self._rooms = {}
		self._networkService = ServerNetwork(self._host, self._port)
	
	"""
		JSON form:
		Form:
			message=
				{
					"command": "",
					"alias": "",
					"address": "",
					"room": "",
					"message":""
				}
	"""

	def parse_incoming(self, in_json):
		cmd_data = json.loads(in_json)
		logging.info("Command:" + cmd_data["command"]+
				" Alias:" + cmd_data ["alias"] +
				" Address:" + cmd_data["address"] +
				" Room:" + cmd_data["room"]+
				" Message:" + str(cmd_data["message"])
				)
		for item in cmd_data:
			item = str(item)
		return cmd_data
		
	def execute_cmd(self, cmd):
		if(cmd["command"] == "C"): #Create
			return self.create_room(cmd)
		elif(cmd["command"] == "J"): #Join
			return self.join_room(cmd)
		elif(cmd["command"] == "L"): #Leave
			return self.leave_room(cmd)
		elif(cmd["command"] == "S"): #Send
			return self.send_message(cmd)
		else:
			logging.debug("Invalid command:" + cmd["command"])
			return False

	#Main Handling Logic of ChatManager
	def run(self):
		pass

	#These functions should follow architecture with parameters
	def create_room(self, cmd):
		logging.info("Creating Room: " + cmd["room"])
		
		if cmd["room"] in self._rooms:
			logging.debug("Room: " + cmd["room"]+ " already exists")
			return False

		self._rooms[cmd["room"]] = Room(cmd["address"],cmd["alias"],cmd["room"])
		logging.info("Room(Name:"+ cmd["room"]+") Created")
		return True
		
	def join_room(self,cmd):
		logging.info("ChatManager: Join Room")
		# catch exception for room not existing
		# return ints for error code
		return self._rooms[cmd["room"]].add_user(cmd["address"],cmd["alias"])
		
	def leave_room(self,cmd):
		logging.info("ChatManager: Leave Room")
		#catch exception for room not existing
		return self._rooms[cmd["room"]].remove_user(cmd["address"],cmd["alias"])
		
	def send_message(self,cmd):
		logging.info("ChatManager: Send message")

		addresses=self._rooms[cmd["room"]].get_address_list
		self._networkService.send_message(addresses,cmd["message"])
	
	def get_room(self,room_name):
		return self._rooms[room_name]

	def __del__(self):
		self._networkService.shutdown()


