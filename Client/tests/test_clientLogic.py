import unittest, hashlib, json, pickle
import clientLogic as L


class TestClientLogic(unittest.TestCase):

    def test_pswHash(self):
        hashgen = hashlib.sha512()
        hashgen.update('admin'.encode('utf8'))
        self.assertEqual(L.generatePswHash('admin'),hashgen.digest())

    def test_decodeQuery(self):
        self.assertEqual(L.decodeServerResponse(json.dumps({'control':'error','content':'test'})),'test')
        self.assertEqual(L.decodeServerResponse(json.dumps({'control':'success','content':'test2'})),'test2')
        self.assertIsNone(L.decodeServerResponse(b'hello'))
        self.assertIsNone(L.decodeServerResponse(json.dumps({'control':'wrong','content':'test3'})))

    def test_patient_sendParams(self): 
        self.assertEqual(L.patient_sendParams('test'),json.dumps({'control':'new_report','content':['test',]}))
        self.assertEqual(L.patient_sendParams('test',['params',]),json.dumps({'control':'new_report','content':['test',['params',]]}))

    def test_sendLoginCredentials(self):
        self.assertEqual(L.sendLoginCredentials('User',b'Password'),pickle.dumps({'control':'login','content':['User',b'Password']}))

    def test_admin_createUser(self):
        self.assertEqual(L.admin_createUser("Name",b'psw',0),pickle.dumps({'control':'add_user','content':("Name",b'psw',0)}))

    def test_admin_deleteUser(self):
        self.assertEqual(L.admin_deleteUser(0),json.dumps({'control':'delete_user','content':0}))

if __name__ == "__main__": 
    unittest.main()
