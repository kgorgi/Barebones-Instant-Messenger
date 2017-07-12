

class ClientHandler:

	def __init__(self):
		self.networkService = Networking.Networking()
		
		
		self.room_name = ""
		self.alias_name = ""
		self.messages = []


		client_address = self.networkingService.get_local_address()

	def join_room(room_name, alias):
		join_json = '{"command": "J","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ client_address +'","message": null}'
		
		send_message(join_json)
		
		code = null
		while code == null:
			code = recieve_next_message()
		return int(code)
		
	def create_room(room_name, alias):
		create_json = '{"command": "C","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ client_address +'","message": null}'
		
		send_message(create_json)
		
		code = null
		while code == null:
			code = recieve_next_message()
		return int(code)
		
	def leave_room(room_name, alias):
		leave_json = '{"command": "L","alias": "' + alias + '","address": "'+ room_name +\
		'","room": "'+ client_address +'","message": null}'
		
		
	def update():
		new_message = recieve_next_message()