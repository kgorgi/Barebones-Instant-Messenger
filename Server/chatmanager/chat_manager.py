import json
import logging
from chatmanager.room import Room
from snet.socket_server import ServerNetwork

class ChatManager:
	_host = "134.87.147.243"
	_port = 8000

	def __init__(self):
		logging.basicConfig(level=logging.DEBUG)
		logging.info("Starting ChatManager")
		self._rooms = dict()
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

	def _parse_incoming(self, in_json):
		trimmed_json = in_json.rstrip(" ")
		cmd_data = json.loads(in_json)

		for item in cmd_data:
			item = str(item)

		#Build Reponse String
		log_str = ""
		for key, item in cmd_data.items():
			log_str = log_str + str(key) + ":" + str(item) + " "

		return cmd_data
		
	def _execute_cmd(self, cmd):
		if(cmd["command"] == "C"): #Create
			result = 0
			if not self.create_room(cmd):
				result = 2 #Room Exists
			self.send_response(cmd["address"], result)
		elif(cmd["command"] == "J"): #Join
			self.send_response(cmd["address"], self.join_room(cmd))
		elif(cmd["command"] == "L"): #Leave
			self.leave_room(cmd)
		elif(cmd["command"] == "S"): #Send
			self.send_message(cmd)
		else:
			logging.debug("Invalid command:" + cmd["command"])
			return False
		return True

	#Main Handling Logic of ChatManager
	def run(self):
		try:
			while(True):
				next_msg = None
				while next_msg is None:
					next_msg = self._networkService.retrieve_next_message()

				command = self._parse_incoming(next_msg)
				if not self._execute_cmd(command):
					#Error Occured: Must Implement
					pass
		except KeyboardInterrupt:
			logging.info("Shutting Down ChatManager")
			del self


	#These functions should follow architecture with parameters
	def create_room(self, cmd):
		logging.info("Creating Room: " + cmd["room"])

		if self._room_exists(cmd["room"]):
			logging.debug("Room: " + cmd["room"]+ " already exists")
			return False

		self._rooms[cmd["room"]] = Room(cmd["address"],cmd["alias"],cmd["room"])
		logging.info("Room(Name:"+ cmd["room"]+") Created")
		return True
		
	def join_room(self,cmd):
		logging.info("ChatManager: Join Room")
		if not self._room_exists(cmd["room"]):
			return 3 #Chat Room does not exit

		current_room =self.get_room(cmd["room"])
		if not current_room.add_user(cmd["address"],cmd["alias"]):
			return 1 #Alias Already Exists


		copy = cmd.copy()
		copy["message"] = "The user "+ copy["alias"] + " joined the room"
		self.send_message(copy)
		return 0 #Success
		
	def leave_room(self,cmd):
		logging.info("ChatManager: Leave Room")
		if not self._room_exists(cmd["room"]):
			logging.debug("ChatManger: Room(" + cmd["room"] + ") does not exist")
			return  # Chat Room does not exit

		current_room = self.get_room(cmd["room"])
		if not current_room.remove_user(cmd["address"],cmd["alias"]):
			logging.debug("ChatManger: Deleting User(" + cmd["alias"] + ") does not exist")
			return

		if current_room.is_empty():
			logging.info("ChatManager: Removing Room (" + cmd["room"] + ")")
			self._rooms.pop(cmd["room"])

		copy = cmd.copy()
		copy["message"] = "The user " + copy["alias"] + " left the room"
		self.send_message(copy)
		
	def send_message(self,cmd):
		logging.info("ChatManager: Send message")

		addresses=self._rooms[cmd["room"]].get_address_list()
		self._networkService.send_message(addresses,cmd["message"])

	def send_response(self, address, res):
		self._networkService.send_response(address, str(res))

	def get_room(self,room_name):
		return self._rooms[room_name]

	def __del__(self):
		self._networkService.shutdown()

	def _room_exists(self, room):
		if room in self._rooms:
			return True
		return False
