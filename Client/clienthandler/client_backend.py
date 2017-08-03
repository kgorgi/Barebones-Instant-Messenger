from abc import ABCMeta, abstractmethod

class ClientBackend:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def join_room(self, room_name, alias): raise NotImplementedError

    @abstractmethod
    def create_room(self,room_name, alias): raise NotImplementedError

    @abstractmethod
    def leave_room(self): raise NotImplementedError

    @abstractmethod
    def update(self): raise NotImplementedError

    @abstractmethod
    def send_message(self, msg): raise NotImplementedError

    @abstractmethod
    def connected(self): raise NotImplementedError