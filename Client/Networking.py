from abc import ABCMeta, abstractmethod

class Networking:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def send_message(self, msg): raise NotImplementedError

    @abstractmethod
    def receive_next_message(self): raise NotImplementedError
