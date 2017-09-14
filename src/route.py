from src.handler import IndexHandler as Index
from src.handler import UserHandler as User
from src.handler import TaskHandler as Task
# from server.handler import ArticleHandler as Article
# from server.handler import PageHandler as Page
# from server.handler import AdminHandler as Admin

route = [
    (r'/', Index.index),
    (r'/index', Index.index),
]

route += [
    (r'/users', User.index),
    (r'/users/<uid:\w{24}>', User.user),
    (r'/users/<uid:\w{24}>/me', User.me),
    (r'/users/<uid:\w{24}>/updatePassword', User.updatePassword),
    (r'/users/<objectid:\w{24}>/refreshSessionToken', User.refreshSessionToken),
    # (r'/users/me', User.index),
    (r'/login', User.login),
]

route += [
    (r'/tasks/', Task.index),
]
#
# route += [
#     (r'/login', User.login),
#     (r'/logout', User.logout)
# ]
#
# route += [
#     (r'/articles', Article.index),
#     (r'/articles/update/<article_id:int>', Article.update),
#     (r'/articles/delete', Article.delete),
#     (r'/articles/create', Article.create),
#     (r'/articles/generate', Article.generate),
# ]
#
# route += [
#     (r'/pages', Page.index),
# ]
#
# route += [
#     (r'/admin', Admin.index),
# ]
