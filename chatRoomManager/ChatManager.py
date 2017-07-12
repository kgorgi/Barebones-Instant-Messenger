import Room
import json

class ChatManager:
	
	def __init__(self):		#add netServiceParams when ready
		self.rooms={}
		#self.networkService=Networking.Networking(params) -- add when ready
		#main()
	
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
	
	def parse_incoming(self,in_json):
		cmd_data = json.loads(in_json)
		deprint("Command:"+cmd_data["command"]+" Alias:"+cmd_data["alias"]+" Address:"+cmd_data["address"]+" Room:"+cmd_data["room"]+" Message:"+str(cmd_data["message"]))
		for each in cmd_data:
			each=str(each)
		return cmd_data
		
	def execute_cmd(self,cmd):
		if(cmd["command"]=="C"):#Create
			return self.create_room(cmd)
		elif(cmd["command"]=="J"):#Join
			return self.join_room(cmd)
		elif(cmd["command"]=="L"):#Leave
			return self.leave_room(cmd)
		elif(cmd["send"]=="S"):#Send
			return self.send_message(cmd)
		else:
			print("invalid command")
			return False
	
	def create_room(self,cmd):
		deprint("Create Room")
		
		for each in self.rooms:
			if(each.get_name==cmd["room"]):
				deprint("Room already Exists")
				return False
		
		self.rooms[cmd["room"]]=Room.Room(cmd["address"],cmd["alias"],cmd["room"])
		deprint("Room Created")
		return True
		
	def join_room(self,cmd_data):
		deprint("Join Room")
		#catch exception for room not existing
		return self.rooms[cmd["room"]].add_user(cmd["address"],cmd["alias"])
		
	def leave_room(self,cmd_data):
		deprint("Leave Room")
		#catch exception for room not existing
		return self.rooms[cmd["room"]].remove_user(cmd["address"],cmd["alias"])
		
	def send_message(self,cmd_data):
		deprint("Send message")
		
		addresses=self.rooms[cmd["room"]].get_address_list
		#send_message(addresses,cmd["message"])
		return True

		
	"""
	def main(): #Put at the bottom
		
			while(True):
				json=*getnextmsg
				data=self.parse_incoming(json)
				error=self.execute_cmd(data)
				send_error(data["address"],error)
	"""		

	
	
if __name__=='__main__':
		#self.__init__()
		#self.main()
		print("Need to implment networkin still, see TestChatManager for trial runs")
		
def deprint(string):
	print(string)
		
		
