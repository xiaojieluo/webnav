import unittest
import requests
from tests.config import CONFIG
from tests.auth import Auth


class IndexTestCase(unittest.TestCase):

    def setUp(self):
        self.url = CONFIG['url']

    def test_index(self):
        '''测试 API 首页数据'''
        url = self.url
        data = {
            'current_user_url': url + '/user',
            'user_url': url + 'users/{users}',
            'user_login': url + '/login'
        }
        r = requests.get(url, auth=Auth())
        self.assertEqual(r.json(), data)

    # def test_authorized(self):
    #     r = requests.get(self.url, auth=Auth())
    #     self.assertEqual(200, r.status_code)
    #
    # def test_unauthorized(self):
    #     r = requests.get(self.url)
    #     self.assertEqual({'msg': 'Unauthorized'}, r.json())
    #
    # def test_code_error_401(self):
    #     r = requests.get(self.url)
    #     self.assertTrue(401, r.status_code)


if __name__ == '__main__':
    unittest.main()
