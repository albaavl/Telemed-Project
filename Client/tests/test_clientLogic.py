import unittest, hashlib
import clientLogic as L

class TestClientLogic(unittest.TestCase):

    def test_pswHash(self):
        hashgen = hashlib.sha512()
        hashgen.update('admin'.encode('utf8'))
        self.assertEqual(L.generatePswHash('admin'),hashgen.digest())

    def test_symptomsQuery(self):
        self.assertEqual(L.generateParamsQuery("hi"),b'hi')
        #TODO

if __name__ == "__main__": 
    unittest.main()
