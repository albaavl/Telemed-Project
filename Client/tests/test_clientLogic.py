import unittest, hashlib, pickle
import clientLogic as L


class TestClientLogic(unittest.TestCase):

    def test_pswHash(self):
        hashgen = hashlib.sha512()
        hashgen.update('admin'.encode('utf8'))
        self.assertEqual(L.generatePswHash('admin'),hashgen.digest())

    def test_decodeQuery(self):
        self.assertEqual(L.decodeServerResponse(pickle.dumps({'control':'error','content':'test'})),'test')
        self.assertEqual(L.decodeServerResponse(pickle.dumps({'control':'success','content':'test2'})),'test2')
        self.assertIsNone(L.decodeServerResponse(b'hello'))
        self.assertIsNone(L.decodeServerResponse(pickle.dumps({'control':'wrong','content':'test3'})))

    def test_sendParams(self): 
        self.assertEqual(L.sendParams('test'),pickle.dumps({'control':'new_report','content':['test',]}))
        self.assertEqual(L.sendParams('test',['params',]),pickle.dumps({'control':'new_report','content':['test',['params',]]}))

    def test_sendLoginCredentials(self):
        self.assertEqual(L.sendLoginCredentials('User',b'Password'),pickle.dumps({'control':'login','content':['User',b'Password']}))

if __name__ == "__main__": 
    unittest.main()
