import unittest
import requests
from tests.auth import Auth
from tests.config import CONFIG
from src.model import User
import json

class UserApi(object):
    '''抽象的用户接口'''
    def __init__(self, url):
        self.url = url

    def login(self, data):
        '''登录'''
        res = requests.post(self.url + '/login', auth=Auth(), json=data)
        return res.json()

    def register(self, data):
        '''注册'''
        res = requests.post(self.url + '/users', auth=Auth(), json=data)
        return res

    def delete(self, data):
        '''删除'''
        login = self.login(data)
        res = requests.delete(self.url + '/users/{objectid}'.format(objectid=login.get('objectid')),
            auth=Auth({'X-LC-Session':login.get('sessionToken')}))

        return res.json()

class TestUser(unittest.TestCase):

    def setUp(self):
        self.url = CONFIG['url']
        self.app = UserApi(self.url)
        self.data = {'username':'test_account','password':'test_password'}

    def test_register(self):
        '''测试注册'''
        res = self.app.register(self.data)
        assert res.status_code == 201

    def test_delete(self):
        res = self.app.delete(self.data)
        print(res)
