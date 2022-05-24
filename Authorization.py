import time
import requests
import json
import sys


class Authorization:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
        })

    def get_authorization(self):
        data = {
            'track_client_id': 'false','recaptcha_pass_token': None,'email': None,'l_username': self.login,'l_password': self.password,'jlog': '1','r': None,'l_remember_me': '1'
        }
        resp = self.session.post('https://kwork.ru/api/user/login', data=data).json()
        self.test_authorization(resp)
        self.save_cookie_authorization()

    @staticmethod
    def test_authorization(resp):
        if resp['success']:
            print('Вы успешно вошли в аккаунт')
        else:
            print('Вы не вошли в аккаунт')
            time.sleep(5)
            sys.exit()

    def save_cookie_authorization(self):
        with open('Kwork_Cookies.json', 'w') as f:
            json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)


def main():
    data_input = open("LoginPassword.txt").read().split()
    auth = Authorization(data_input[0], data_input[1])
    auth.get_authorization()


if __name__ == '__main__':
    main()

input()



