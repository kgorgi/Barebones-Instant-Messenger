import json
from clienthandler.client_backend import ClientBackend
from cnet.socket_client import ClientNetworking
import logging

class ClientHandler(ClientBackend):
    SUCCESS = "0"

    def __init__(self):
        self._networkService = ClientNetworking("127.0.0.1", 8000)
        self.room_name = ""
        self.alias_name = ""
        self.client_address = self._networkService.get_local_address()

    def join_room(self, room_name, alias):
        logging.info("Attempting to join the room " + room_name)
        join_json = self._create_instruction("J", alias, room_name, None)
        self._networkService.send_message(join_json)
        server_feedback = self._get_server_feedback()
        
        if server_feedback is self.SUCCESS:
            self.room_name = room_name
            self.alias_name = alias
            logging.info("Successfully joined the room " + room_name)

        return int(server_feedback)
		
    def create_room(self,r_name, alias):
        create_json = self._create_instruction("C", alias, r_name, None)
        self._networkService.send_message(create_json)
        logging.info("Attempting to create the room " + r_name)
        server_feedback = self._get_server_feedback()

        if server_feedback is self.SUCCESS:
            self.room_name = r_name
            self.alias_name = alias
            logging.info("Successfully created the room " + r_name)

        return int(server_feedback)
		
    def leave_room(self):
        logging.info("Leaving the room " + self.room_name)
        leave_json = self._create_instruction("L", self.alias_name, self.room_name, None)
        self._networkService.send_message(leave_json)

    def quit(self):
        logging.info("Quitting the program")
        quit_json = self._create_instruction("Q", self.alias_name, self.room_name, None)
        self._networkService.send_message(quit_json)

    def update(self):
        new_message = self._networkService.receive_next_message()
        if not new_message is None:
            new_message = new_message

        return new_message

    def connected(self):
        #logging.info("The server is connected: "+ str(self._networkService.is_connected))
        return self._networkService.connected_to_server()


    def send_message(self, msg):
        logging.info("Sending message \"" + msg + "\"")
        message_json = self._create_instruction("S", self.alias_name, self.room_name, self.alias_name + ": " + msg)
        msg_length= len(message_json)
        message_json = message_json + ' ' * (280 - msg_length)
        self._networkService.send_message(message_json)

    def _create_instruction(self, command, alias, room, msg):
        message = {
            "command": command,
            "alias": alias,
            "address": self.client_address,
            "room": room,
            "message": msg
        }

        return json.dumps(message)

    def _get_server_feedback(self):
        server_feedback = None
        while server_feedback is None:
            server_feedback = self._networkService.receive_next_message()

        return server_feedback
