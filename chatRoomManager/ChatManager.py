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
			self.create_room(cmd)
		elif(cmd["command"]=="J"):#Join
			self.join_room(cmd)
		elif(cmd["command"]=="L"):#Leave
			self.leave_room(cmd
		elif(cmd["command"]=="S"):#Send
			self.send_message(cmd)
		else:
			print("invalid command")
			return False
	
	def create_room(self,cmd):
		deprint("Create Room")
		
		for each in rooms:
			if(each.get_name==cmd["room"]):
				deprint("Room already Exists")
				return False
		
		rooms[cmd["room"]]=Room.room(cmd["address"],cmd["alias"],cmd["room"])
		deprint("Room Created")
		return True
		
	def join_room(self,cmd_data):
		deprint("Join Room")
		#catch exception for room not existing
		return rooms[cmd["room"]].add_user(cmd["address"],cmd["alias"])
		
	def leave_room(self,cmd_data):
		deprint("Leave Room")
		rooms[cmd["room"]].remove_user(cmd["address"],cmd["alias"])
		
	def Send_message(self,cmd_data):
		deprint("Send message")
		

		
		
	#def main(): #Put at the bottom


	
	
if __name__=='__main__':
		#main()
		print("Wait")
		
def deprint(string):
	print(string)
		
		
