import unittest

class TestBananaRecipes(unittest.TestCase):
    def test_banana_pudding(self):
        self.assertEqual(banana_pudding(), "Banana Pudding recipe ready!")

    def test_rot13_encryptor(self):
        self.assertEqual(rot13_encryptor("test"), "uryyb")

if __name__ == '__main__':
    unittest.main()
