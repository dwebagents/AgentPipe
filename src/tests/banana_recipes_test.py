import unittest
from recipes.banana_pudding import BananaPudding

class TestBananaPudding(unittest.TestCase):
    def setUp(self):
        self.banana_pudding = BananaPudding()

    def test_create_banana_pudding(self):
        # Write test cases for creating a banana pudding
        self.assertEqual(len(self.banana_pudding.ingredients), 0)

if __name__ == '__main__':
    unittest.main()
