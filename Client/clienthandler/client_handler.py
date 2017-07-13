from networking.client_networking import ClientNetworking
class ClientHandler:

	def __init__(self):
		self._networkService = ClientNetworking()
		
		
		self.room_name = ""
		self.alias_name = ""
		self.messages = []


		self.client_address = self.networkingService.get_local_address()

	def join_room(self, room_name, alias):
		join_json = '{"command": "J","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ self.client_address +'","message": null}'
		
		self._networkService.send_message(join_json)
		
		code = None
		while code == None:
			code = self._networkServicerecieve_next_message()
		return int(code)

		if code is "0":
			self.room_name = room_name
			self.alias_name = alias
		
	def create_room(self,room_name, alias):
		create_json = '{"command": "C","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ self.client_address +'","message": null}'
		
		self._networkService.send_message(create_json)
		
		code = None
		while code == None:
			code = self._networkService.recieve_next_message()
		return int(code)
		
	def leave_room(self,room_name, alias):
		leave_json = '{"command": "L","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ self.client_address +'","message": null}'
		
		
	def update(self):
		new_message = self._networkServicerecieve_next_message()

	def send_message(self, msg):
		self._networkService.send_message(msg)
