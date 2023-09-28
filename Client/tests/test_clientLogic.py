import unittest, hashlib, pickle
import clientLogic as L

class TestClientLogic(unittest.TestCase):

    def test_pswHash(self):
        hashgen = hashlib.sha512()
        hashgen.update('admin'.encode('utf8'))
        self.assertEqual(L.generatePswHash('admin'),hashgen.digest())

    def test_symptomsQuery(self):
        self.assertEqual(L.generateParamsQuery("hi"),pickle.dumps({'control':'new_report','content':"hi"}))

    def test_decodeQuery(self):
        self.assertEqual(L.decodeQuery(pickle.dumps({'control':'error','content':'test'})),'test')
        self.assertEqual(L.decodeQuery(pickle.dumps({'control':'success','content':'test2'})),'test2')
        self.assertIsNone(L.decodeQuery(b'hello'))
        self.assertIsNone(L.decodeQuery(pickle.dumps({'control':'wrong','content':'test3'})))

    def test_generateParamsQuery(self): #TODO not sure if this format will fly :)
        self.assertEqual(L.generateParamsQuery('test'),pickle.dumps({'control':'new_report','content':'test'}))
        self.assertEqual(L.generateParamsQuery('test','params'),pickle.dumps({'control':'new_report','content':'<symptoms:>test<data:>params'}))

if __name__ == "__main__": 
    unittest.main()
