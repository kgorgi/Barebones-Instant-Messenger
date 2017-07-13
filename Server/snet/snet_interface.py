from abc import ABCMeta, abstractmethod

class Networking():

    @abstractmethod
    def send_response(self, address, error):
        raise NotImplementedError

    @abstractmethod
    def send_message(self, addresses, msg):
        raise NotImplementedError

    @abstractmethod
    def retrieve_next_message(self):
        raise NotImplementedError
