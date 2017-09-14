from sanic.response import json, text
from mongoengine.errors import NotUniqueError
import datetime
import json as pyjson
from bson import json_util
from copy import deepcopy

# src module
from handler import APIHandler
from model import User, Task
from web import error, generateSessionToken, log, AccountLock, validate, Authenticated, AuthenticatedError

class index(APIHandler):

    def get(self, requests):
        '''任务查询'''
        where = self.query_constraint(requests)
        # 返回的不是数组，就表示出现错误了
        if isinstance(where, tuple):
            return error(where[0], {'msg': where[1]})

        users = list()
        for user in User.get_users(where):
            users.append(user)

        data = {
            'body': {'results': users}
        }
        return json(**data)

    def post(self, requests):
        '''新建任务'''
        data = requests.json
        # 检测用户是否登录
        session = requests.headers.get('X-LC-Session')
        where = self.query_constraint(requests)
        user = next(User.get_users(where, sessionToken=session, raw=True)).first()

        if user is None:
            return error(211)

        if not isinstance(data, dict) or data is None:
            return error(107)

        if 'title' not in data:
            return error(301)
        # if User.objects(username=request['username']).first() is not None:
        #     return error(202)

        # 生成 sessionToken
        # sessionToken = generateSessionToken()
        data.update({
            # 'title': data.get('title').decode('utf-8'),
            # 'desc': data.get('desc').decode('utf-8'),
            'own': user.id,
            'createdAt': datetime.datetime.utcnow(),
            'updatedAt': datetime.datetime.utcnow(),
        })
        print(data)
        task = Task(**data)
        task.save()

        body = deepcopy(data)
        body.update({
            # 'title': body['title'].encode('utf-8'),
            'own': str(body['own']),
            'createdAt': data['createdAt'].isoformat(),
            'updatedAt': data['updatedAt'].isoformat()
        })

        # print(body)
        result = {
            'body': body,
            'headers': {'Location': '/tasks/{}'.format(task.id)},
            'status': 201
        }
        # print(result)
        # return text(str(result))
        return json(**result)
        # task = Task(**)
