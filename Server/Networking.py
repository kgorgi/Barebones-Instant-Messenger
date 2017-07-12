from abc import ABCMeta, abstractmethod

class Networking():
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def send_error(self, address, error):
        raise NotImplementedError

    @abstractmethod
    def send_message(self, addresses, msg):
        raise NotImplementedError

    @abstractmethod
    def retrieve_next_message(self):
        raise NotImplementedError
