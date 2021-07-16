import requests
import unittest
import json


class ApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = 'http://xfpapi.ykb100.com/api/auth/login'

    @classmethod
    def tearDownClass(cls):
        pass

    def write_token(self):
        """将Token信息写入Token.md文件中"""
        data = {"userName": 13062200301,
                'saasCode': '000009',
                # 'deviceId': device,
                "password": 12345678}
        response = requests.post(url=self.url,
                                 json=data,
                                 data=json.dumps(data,
                                                 ensure_ascii=False),
                                 headers={
                                      'Content-Type': 'application/json'

                                  })
        with open('Token.md', 'w') as f:
            f.write(response.json()['token'])

    def read_Token(self):
        """读取Token.md文件中的Token信息"""
        with open('Token.md', 'r') as f:
            return f.read()

    def test_getApiTask(self):
        """验证获取所有任务接口"""
        response = requests.get(url=self.url + '11',
                                headers=self.read_Token())
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)



