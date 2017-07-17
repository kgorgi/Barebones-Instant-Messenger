import json
import socket
from clienthandler.client_backend import ClientBackend
from cnet.socket_client import ClientNetworking


class ClientHandler(ClientBackend):

    #Server feedback codes
    SUCCESS = "0"

    def __init__(self):
        self._networkService = ClientNetworking("134.87.139.78", 8000)
        self.room_name = ""
        self.alias_name = ""
        self.messages = []
        self.client_address = self._networkService.get_local_address()

    def join_room(self, room_name, alias):
        join = {
            "command": "J",
            "alias": alias,
            "address": self.client_address,
			"room": room_name,
			"message": None
		}

        join_json = json.dumps(join)
        self._networkService.send_message(join_json)
		
        server_feedback = None
        while server_feedback is None:
            server_feedback = self._networkService.receive_next_message()

        if server_feedback is self.SUCCESS:
            self.room_name = room_name
            self.alias_name = alias

        return int(server_feedback)
		
    def create_room(self,r_name, alias):
        create = {
			"command": "C",
			"alias": alias,
            "address": self.client_address,
            "room": r_name,
			"message": None
		}

        create_json = json.dumps(create)
        self._networkService.send_message(create_json)
		
        server_feedback = None
        while server_feedback is None:
            server_feedback = self._networkService.receive_next_message()

        if server_feedback is self.SUCCESS:
            self.room_name = r_name
            self.alias_name = alias

        return int(server_feedback)
		
    def leave_room(self):

        leave = {
			"command": "L",
			"alias": self.alias_name,
            "address": self.client_address,
            "room": self.room_name,
			"message": None
		}

        leave_json = json.dumps(leave)
        self._networkService.send_message(leave_json)

    def update(self):
        new_message = self._networkService.receive_next_message()
        return new_message

    def send_message(self, msg):
        message = {
			"command": "S",
			"alias": None,
			"address": self.client_address,
			"room": self.room_name,
			"message": self.alias_name + ": " + msg
		}

        message_json = json.dumps(message)
        self._networkService.send_message(message_json)
