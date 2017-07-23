import json
import socket
from clienthandler.client_backend import ClientBackend
from cnet.socket_client import ClientNetworking


class ClientHandler(ClientBackend):

    #Server feedback codes do this devlyn
    SUCCESS = "0"

    def __init__(self):
        self._networkService = ClientNetworking("127.0.0.1", 8000)
        self.room_name = ""
        self.alias_name = ""
        self.client_address = self._networkService.get_local_address()

    def join_room(self, room_name, alias):
        join_json = self.create_instruction("J", alias, room_name, None)
        self._networkService.send_message(join_json)
		
        server_feedback = None
        while server_feedback is None:
            server_feedback = self._networkService.receive_next_message()
        
        server_feedback = server_feedback
        
        if server_feedback is self.SUCCESS:
            self.room_name = room_name
            self.alias_name = alias

        return int(server_feedback)
		
    def create_room(self,r_name, alias):
        create_json = self.create_instruction("C", alias, r_name, None)
        self._networkService.send_message(create_json)
		
        server_feedback = None
        while server_feedback is None:
            server_feedback = self._networkService.receive_next_message()
        
        server_feedback = server_feedback

        if server_feedback is self.SUCCESS:
            self.room_name = r_name
            self.alias_name = alias

        return int(server_feedback)
		
    def leave_room(self):
        leave_json = self.create_instruction("L", self.alias_name, self.room_name, None)
        self._networkService.send_message(leave_json)
    
        server_feedback = self._networkService.receive_next_message()
        while server_feedback is not None:
            server_feedback = self._networkService.receive_next_message()


    def quit(self):
        quit_json = self.create_instruction("Q", self.alias_name, self.room_name, None)
        self._networkService.send_message(quit_json)



    def update(self):
        new_message = self._networkService.receive_next_message()
        if not new_message is None:
            new_message = new_message


        return new_message

    def send_message(self, msg):
        message_json = self.create_instruction("S", self.alias_name, self.room_name, self.alias_name + ": " + msg)
        msg_length= len(message_json)
        message_json = message_json + ' ' * (280 - msg_length)
        self._networkService.send_message(message_json)

    def create_instruction(self, command, alias, room, msg):
        message = {
            "command": command,
            "alias": alias,
            "address": self.client_address,
            "room": room,
            "message": msg
        }

        message_json = json.dumps(message)
        return message_json


