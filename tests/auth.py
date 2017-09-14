from requests.auth import AuthBase


class Auth(AuthBase):
    def __init__(self, *args, **kw):
        self.id = 'FFnN2hso42Wego3pWq4X5qlu'
        self.sign = 'd5bcbb897e19b2f6633c716dfdfaf9be,1453014943466'
        # print(args)
        self.args = list()
        for k in args:
            self.args.append(k)

    def __call__(self, r):
        r.headers['X-LC-Id'] = self.id
        r.headers['X-LC-Sign'] = self.sign
        for k in self.args:
            for key, value in k.items():
                r.headers[key] = value

        return r
