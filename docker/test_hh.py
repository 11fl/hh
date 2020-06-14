import unittest
import hhparce

class TestHH(unittest.TestCase):

    def test_re2(self):
        string = '200 000-200 000 руб.'
        result = hhparce.reg(string)
        self.assertEqual(result, 200000)
    
    def test_re1(self):
        string = 'до 150 000 руб.'
        result = hhparce.reg(string)
        self.assertEqual(result, 150000)

if __name__ == "__main__":
    unittest.main()