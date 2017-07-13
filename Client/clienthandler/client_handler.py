from networking.client_networking import ClientNetworking
class ClientHandler:

	def __init__(self):
		self._networkService = ClientNetworking()
		
		
		self.room_name = ""
		self.alias_name = ""
		self.messages = []


		self.client_address = self.networkingService.get_local_address()

	def join_room(self, room_name, alias):
		join = {
			"command": "J",
			"alias": alias,
			"address": room_name,
			"room": self.client_address,
			"message": null
		}

		join_json = json.dumps(join)

		self._networkService.send_message(join_json)
		
		code = None
		while code is None:
			code = self._networkServicerecieve_next_message()

		if code is "0":
			self.room_name = room_name
			self.alias_name = alias

		return int(code)
		
	def create_room(self,room_name, alias):
		create = {
			"command": "C",
			"alias": alias,
			"address": room_name,
			"room": self.client_address,
			"message": null
		}

		create_json = json.dumps(create)
		self._networkService.send_message(create_json)
		
		code = None
		while code is None:
			code = self._networkService.recieve_next_message()

		if code is "0":
			self.room_name = room_name
			self.alias_name = alias

		return int(code)
		
	def leave_room(self):

		leave = {
			"command": "L",
			"alias": self.alias,
			"address": self.room_name,
			"room": self.client_address,
			"message": null
		}

		leave_json = json.dumps(leave)
		self._networkService.send_message(leave_json)

	def update(self):
		new_message = self._networkServicerecieve_next_message()

		return new_message

	def send_message(self, msg):
		message = {
			"command": "S",
			"alias": null,
			"address": null,
			"room": self.client_address,
			"message": msg
		}

		message_json = json.dumps(message)

		self._networkService.send_message(message_json)
