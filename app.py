import json
import logging
import os

import flask_login
from flask import Flask, abort, request
from flask.cli import load_dotenv

from controller.UserController import UserController
from entities.User import User
from repo.repository import Repository


def app_factory():
    _app = Flask(__name__)

    load_dotenv()
    _app.secret_key = os.getenv('FLASK_SECRET_KEY')
    _app.config['SESSION_TYPE'] = 'memcached'
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s]\t%(filename)s -> %(funcName)s()\t%(message)s')

    _login_manager = flask_login.LoginManager()
    _login_manager.init_app(_app)
    return _app, _login_manager,


app, login_manager = app_factory()
user_controller = UserController()


# message_repository = MessageRepo()
# chat_repository = ChatRepo()


@login_manager.user_loader
def load_user(username) -> User or None:
    try:
        return user_controller.get_by_username(username)
    except IndexError:
        return None


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/v1/auth/register', methods=['POST'])
def api_user_register():
    data_dict = json.loads(request.data.decode('utf-8'))
    username = data_dict['username']
    password = data_dict['password']
    if user_controller.exists(username):
        return 'Username already in use', 400
    user_controller.create(username, password)
    return 'Success', 200


@app.route('/v1/auth/login', methods=['POST'])
def api_user_login():
    data_dict = json.loads(request.data.decode('utf-8'))
    username = data_dict['username']
    password = data_dict['password']
    if user_controller.is_auth_valid(username, password):
        user_controller.update_authenticated_status(username, True)
        flask_login.login_user(user_controller.get_by_username(username), remember=True)
        return 'Success', 200
    else:
        abort(403, 'Incorrect username or password!')


@app.route('/v1/auth/logout', methods=['POST'])
@flask_login.login_required
def api_user_logout():
    user: User = flask_login.current_user
    user_controller.update_authenticated_status(user.username, False)
    flask_login.logout_user()
    return 'Success', 200


def startup():
    Repository.create_if_necessary()


if __name__ == 'app':
    startup()
if __name__ == '__main__':
    startup()
    app.run()
