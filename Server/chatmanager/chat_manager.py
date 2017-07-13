import json
from chatmanager.room import Room
from networking.server_networking import ServerNetwork

class ChatManager:

	def __init__(self):
		self.rooms = {}
		self.Network = ServerNetwork()
	
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
		
		for room in self.__rooms:
			if(room.get_name() == cmd["room"]):
				deprint("Room already Exists")
				return "Room Exists"



		self.__rooms[cmd["room"]] = Room(cmd["address"],cmd["alias"],cmd["room"])
		deprint("Room(Name:"+cmd["room"]+") Created")
		return 0
		
	def join_room(self,cmd):
		deprint("Join Room")
		#catch exception for room not existing
		return self.__rooms[cmd["room"]].add_user(cmd["address"],cmd["alias"])
		
	def leave_room(self,cmd):
		deprint("Leave Room")
		#catch exception for room not existing
		return self.__rooms[cmd["room"]].remove_user(cmd["address"],cmd["alias"])
		
	def send_message(self,cmd):
		deprint("Send message")
		
		addresses=self.__rooms[cmd["room"]].get_address_list
		self.__Network.send_message(addresses,cmd["message"])
		return 0
	
	def get_room(self,room_name):
    		return self.__rooms[room_name]

		
def deprint(string):
	print(string)
		
		
