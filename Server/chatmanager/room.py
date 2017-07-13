class Room:
    def __init__(self, address, alias, name):
        self.__name = name  # roomName
        self.__user_list = [(address, alias)]

    def add_user(self, address, alias):
        # adds user to room
        for ad, al in self.__user_list:
            if (al == alias): return "User Exists"
        # if(ad == address) return False #This check depends on network

        self.__user_list.append((address, alias))
        return 0

    def remove_user(self, address, alias):
        # Only deletes first instance of alias, doesn't check duplicates
        for user in self.__user_list:
            if (user[1] == alias):
                self.__user_list.remove(user)
                return 0

        return "User Doesnt Exist"

    def get_name(self):
        return self.__name

    def get_address_list(self):
        out = [user[0] for user in self.__user_list]
        return out

    def get_alias_list(self):
        out = [user[1] for user in self.__user_list]
        return out

    def get_user_list(self):
        return self.__user_list