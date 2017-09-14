import os
from sanic.response import json, text, html

# src module
from handler import APIHandler
from web import log

class index(APIHandler):

    async def get(self, requests):
        url = self.config['url']
        data = {
            'current_user_url': url + '/user',
            'user_url': url + 'users/{users}',
            'user_login': url + '/login'
        }
        return json(data)
