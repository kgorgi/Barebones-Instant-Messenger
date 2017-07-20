import json
import logging
import settings
from chatmanager.room import Room
from snet.socket_server import ServerNetwork

class ChatManager:
	_host = "127.0.0.1"
	_port = 8000

	def __init__(self):
		logging.basicConfig(format = settings.ChatServer.get('flog'),level= settings.ChatServer.get('logging'))

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
		cmd_data = json.loads(in_json)

		for item in cmd_data:
			item = str(item)

		#Build Reponse String
		log_str = ""
		for key, item in cmd_data.items():
			log_str = log_str + str(key) + ":" + str(item) + " "

		return cmd_data

	def _send_join_message(self, cmd, response_code):
		if response_code == 0:
			copy = cmd.copy()
			copy["message"] = "The user " + copy["alias"] + " joined the room."
			self.send_message(copy)

	def _execute_cmd(self, cmd):
		if(cmd["command"] == "C"): #Create
			result = 0
			if not self.create_room(cmd):
				result = 2 #Room Exists
			self.send_response(cmd["address"], result)

			self._send_join_message(cmd, result)

		elif(cmd["command"] == "J"): #Join
			response_code = self.join_room(cmd)
			self.send_response(cmd["address"], response_code )
			self._send_join_message(cmd, response_code)
		elif(cmd["command"] == "L" or cmd["command"] == "Q"): #Leave
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
			return 3 #Chat Room Does Not exit

		current_room =self.get_room(cmd["room"])
		if not current_room.add_user(cmd["address"],cmd["alias"]):
			return 1 #Alias Already Exists

		return 0 #Success
		
	def leave_room(self,cmd):
		logging.info("ChatManager: Leave Room")
		room = None
		alias = None

		# User Has Quit Out of the Application or the Connection Has Been Dropped
		if cmd["command"] == "Q":
			#No Alias or Room Specified: Search Manually
			addr = cmd["address"]
			success = False
			for key, r in self._rooms.items():
				if r.address_in_room(addr):
					alias = r.remove_user_by_address(addr)
					room = r
					success = True
					break
			if not success:
				logging.debug("ChatManager: Error Address + " + addr + " not in any room.")
		else:
			room_str = cmd["room"]
			#User Has Left a Chat Room Normally: Room and Alias Provided
			if not self._room_exists(room_str):
				logging.debug("ChatManger: Room(" + room_str + ") does not exist")
				return  # Chat Room does not exit

			alias = cmd["alias"]
			room = self.get_room(room_str)

			if not room.remove_user(cmd["address"], alias):
				logging.debug("ChatManger: Deleting User(" + alias + ") does not exist in room (" + room_str + ")" )
				return

		#Delete Chat Room if it is Empty
		if room != None and room.is_empty():
			logging.info("ChatManager: Removing Room (" + cmd["room"] + ")")
			self._rooms.pop(cmd["room"])
		else:
			copy = cmd.copy()
			copy["message"] = "The user " + alias + " left the room."
			copy["room"] = room.get_name()
			self.send_message(copy)
		
	def send_message(self,cmd):
		logging.info("ChatManager: Send message")

		addresses = self.get_room(cmd["room"]).get_address_list()
		self._networkService.send_message(addresses, cmd["message"])

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
