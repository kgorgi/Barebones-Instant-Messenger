import unittest
from chatmanager.room import Room


class TestRoom(unittest.TestCase):

	def test_initializer(self):
		rm = Room("ad1","alA","newRoom")
		self.assertEqual(rm.get_address_list(),["ad1"])
		self.assertEqual(rm.get_alias_list(), ["alA"])
		self.assertEqual(rm.get_name(),"newRoom")
		
	def test_add_user(self):
		rm = Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		self.assertEqual(rm.get_address_list(),["ad1","ad2"])
		self.assertEqual(rm.get_alias_list(), ["alA", "alB"])
		
	def test_add_user_duplicate(self):
		rm = Room("ad1","alA","newRoom")
		rm.add_user("ad1","al1")
		self.assertFalse(rm.add_user("ad1","al1"))
		
	def test_rm_user(self):
		rm = Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		rm.remove_user("ad1","alA")
		self.assertEqual(rm.get_address_list(),["ad2"])
		self.assertEqual(rm.get_alias_list(),["alB"])
		
	def test_rm_user_duplicate(self):
		rm = Room("ad1","alA","newRoom")
		rm.add_user("ad2","alB")
		self.assertFalse(rm.remove_user("ad3","alC"))
		
	def test_get_address_list(self):
		rm = Room("ad1","al1","newRoom")
		compare = ["ad1"]
		for i in range(2,45):
			ad = "ad"+str(i)
			al = "al"+str(i)
			rm.add_user(ad,al)
			compare.append(ad)
		self.assertEqual(rm.get_address_list(),compare)

	def test_get_alias_list(self):
		rm = Room("ad1", "al1", "newRoom")
		compare = ["al1"]
		for i in range(45, 90):
			ad = "ad" + str(i)
			al = "al" + str(i)
			rm.add_user(ad, al)
			compare.append(al)
		self.assertEqual(rm.get_alias_list(), compare)

	def test_address_in_room(self):
		rm = Room("ad1", "al1", "newRoom")
		self.assertFalse(rm.address_in_room("b2"))
		self.assertTrue(rm.address_in_room("ad1"))

	def test_remove_by_address(self):
		rm = Room("ad1", "alA", "newRoom")
		rm.add_user("ad2", "alB")
		rm.remove_user_by_address("ad1")
		self.assertEqual(rm.get_address_list(), ["ad2"])
		self.assertEqual(rm.get_alias_list(), ["alB"])

if __name__=='__main__':
	unittest.main()