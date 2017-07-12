import unittest
import Room

class TestRoom(unittest.TestCase):

	def test_initializer(self):
		rm = Room.Room("ad1","alA","newRoom")
		self.assertEqual(rm.get_user_list(),[("ad1","alA")])
		self.assertEqual(rm.get_name(),"newRoom")
		
	def test_add_user(self):
		rm = Room.Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		self.assertEqual(rm.get_user_list(),[("ad1","alA"),("ad2","alB")])
		
	def test_add_user_duplicate(self):
		rm = Room.Room("ad1","alA","newRoom")
		rm.add_user("ad1","al1")
		self.assertFalse(rm.add_user("ad1","al1"))
		
	def test_rm_user(self):
		rm = Room.Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		rm.remove_user("ad2","alB")
		self.assertEqual(rm.get_user_list(),[("ad1","alA")])
		
	def test_rm_user_duplicate(self):
		rm = Room.Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		self.assertFalse(rm.remove_user("ad3","alC"))
		
	def test_get_AddressList(self):
		rm = Room.Room("ad1","al1","newRoom")
		compare = ["ad1"]
		for i in range(2,45):
			ad = "ad"+str(i)
			al = "al"+str(i)
			rm.add_user(ad,al)
			compare.append(ad)
		self.assertEqual(rm.get_address_list(),compare)
			
		
		

if __name__=='__main__':
	unittest.main()