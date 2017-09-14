from sanic.views import HTTPMethodView
from sanic.response import json, text, raw, html
from model import User, App
import logging
import hashlib
from sanic.exceptions import InvalidUsage
from web import log
import json as pyjson
from web import error
from config import CONFIG


class APIHandler(HTTPMethodView):

    def __init__(self):
        self.config = CONFIG

    def query_constraint(self, requests):
        '''
        支持查询约束
        '''
        # TODO 文档编写
        # 正常返回数组，出现错误返回元组， (200, 'This is error.')

        args = requests.args

        where = {}
        if 'where' in requests.args:
            where = requests.args.get('where')
            if isinstance(where, str):
                where = pyjson.loads(where)

        order = args.get('order', '')
        keys = args.get('keys', '')
        exclude = []
        only = []

        if keys:
            keys = keys.split(',')
            for k in keys:
                if k[0] == '-':
                    exclude.append(k[1:])
                else:
                    only.append(k)

        try:
            limit = int(args.get('limit', 100))
        except ValueError as e:
            return (500, 'limit must be an integer.')

        try:
            skip = args.get('skip', 400)
        except ValueError:
            return (500, 'skip must be an integer.')

        result = {
            'where': where,
            'order': order,
            'limit': limit,
            'skip': skip,
            # 'keys' : keys
            'exclude' : exclude,
            'only' : only
        }
        return result

    @classmethod
    async def authenticated(cls, requests):
        '''
        用户权限认证
        基于 appid 与 appkey

        appid
        appkey
        '''
        log(requests)
        logging.info('authenticated verification')
        id_name = 'X-LC-Id'
        key_name = 'X-LC-Key'
        sign_name = 'X-LC-Sign'

        headers = requests.headers

        app = App.objects(appid=headers.get(id_name, None)).first()
        # app id 不存在
        if app is None:
            return json({'msg':'Unauthorized'}, 401)

        if sign_name in headers:
            logging.info('use X-LC-Sign to verify application')
            sign = headers.get(sign_name)
            result = cls.SignVerify(cls, sign, app.appkey)
        else:
            logging.info('use X-LC-Id and X-LC-Key to verify application')
            appid = headers.get(id_name, None)
            appkey = headers.get(key_name, None)
            result = cls.KeyVerify(cls, app, appid, appkey)

        if result is False:
            return json({'msg': 'Unauthorized'}, 401)

    def KeyVerify(self, app, appid, appkey):
        # 根据 appid 与 appkey 验证权限
        if isinstance(app, App):
            if app.appid == appid and app.appkey == appkey:
                return True

        return False

    def SignVerify(self, sign, appkey):
        # md5( timestamp + App Key )
        #     = md5( 1453014943466UtOCzqb67d3sN12Kts4URwy8 )
        #     = d5bcbb897e19b2f6633c716dfdfaf9be
        encrypt, timestamp = sign.split(',')
        md5 = hashlib.md5()
        md5.update(timestamp.encode('utf-8') + appkey.encode())

        if md5.hexdigest() == encrypt:
            return True

        return False

    @classmethod
    async def data_integrity_verification(cls, request):
        '''
        数据完整性验证
        '''
        log.info('Data integrity verification')
        # print('Data integrity verification')

    def verifyJson(self, requests):
        print(type(requests.json))
        print(not isinstance(requests.json, dict) or requests.json is None)
        # print(requests.json)
        # if requests.json is not None:
        # try:
        #     requests.json
        # except InvalidUsage as e:
        #     return json({'code':107, 'error':'Malformed json object. A json dictionary is expected.'})
        if not isinstance(requests.json, dict) or requests.json is None:
            return json({'code': 107, 'error': 'Malformed json object. A json dictionary is expected.'})

        return None
