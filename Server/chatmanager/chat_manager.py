import json
from chatmanager.room import Room
from snet.socket_server import ServerNetwork

class ChatManager:
	_host = "127.0.0.1"
	_port = 8000

	def __init__(self):
		self._rooms = {}
		self._network = ServerNetwork(self._host, self._port)
	
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
		deprint("Command:"+cmd_data["command"]+
				" Alias:"+cmd_data["alias"]+
				" Address:"+cmd_data["address"]+
				" Room:"+cmd_data["room"]+
				" Message:"+str(cmd_data["message"])
				)
		for item in cmd_data:
			item = str(item)
		return cmd_data
		
	def execute_cmd(self, cmd):
		if(cmd["command"] == "C"):#Create
			return self.create_room(cmd)
		elif(cmd["command"] == "J"):#Join
			return self.join_room(cmd)
		elif(cmd["command"] == "L"):#Leave
			return self.leave_room(cmd)
		elif(cmd["send"] == "S"):#Send
			return self.send_message(cmd)
		else:
			print("invalid command")
			return False
	
	def create_room(self, cmd):
		deprint("Creating Room: "+cmd["room"])
		
		for room in self._rooms:
			if(room.get_name() == cmd["room"]):
				deprint("Room already Exists")
				return "Room Exists"



		self._rooms[cmd["room"]] = Room(cmd["address"],cmd["alias"],cmd["room"])
		deprint("Room(Name:"+cmd["room"]+") Created")
		return 0
		
	def join_room(self,cmd):
		deprint("Join Room")
		#catch exception for room not existing
		return self._rooms[cmd["room"]].add_user(cmd["address"],cmd["alias"])
		
	def leave_room(self,cmd):
		deprint("Leave Room")
		#catch exception for room not existing
		return self._rooms[cmd["room"]].remove_user(cmd["address"],cmd["alias"])
		
	def send_message(self,cmd):
		deprint("Send message")
		
		addresses=self._rooms[cmd["room"]].get_address_list
		self._network.send_message(addresses,cmd["message"])
		return 0
	
	def get_room(self,room_name):
    		return self._rooms[room_name]

	def __del__(self):
		self._network.shutdown()

def deprint(string):
	print(string)

