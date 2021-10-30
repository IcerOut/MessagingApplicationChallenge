import json
import logging
import os
from json import JSONDecodeError

import flask_login
from flask import Flask, abort, request, send_from_directory

import CONSTANTS
from controller.ChatController import ChatController
from controller.MessageController import MessageController
from controller.UserController import UserController
from entities.User import User
from repo.Repository import Repository


def app_factory():
    _app = Flask(__name__)

    _app.secret_key = 'Parakeet-Douche-Underpaid-Gulp4'
    _app.config['SESSION_TYPE'] = 'memcached'
    logging.basicConfig(level=logging.INFO,
                        format='[%(levelname)s]\t%(filename)s -> %(funcName)s()\t%(message)s')

    _login_manager = flask_login.LoginManager()
    _login_manager.init_app(_app)
    return _app, _login_manager


app, login_manager = app_factory()
user_controller = UserController()
chat_controller = ChatController()
message_controller = MessageController()


@login_manager.user_loader
def load_user(username) -> User or None:
    try:
        return user_controller.get_by_username(username)
    except IndexError:
        return None


# <editor-fold desc="Routes">
# <editor-fold desc="Auth Routes">
@app.route('/v1/auth/register', methods=['POST'])
def api_user_register():
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', 400
    try:
        username = data_dict['username']
        password = data_dict['password']
    except KeyError:
        return 'Malformed request', 400
    if user_controller.exists(username):
        return 'Username already in use', 400
    user_controller.create(username, password)
    return 'Success', 200


@app.route('/v1/auth/login', methods=['POST'])
def api_user_login():
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', 400
    try:
        username = data_dict['username']
        password = data_dict['password']
    except KeyError:
        return 'Malformed request', 400
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


# </editor-fold>
# <editor-fold desc="Group Chat Routes">
@app.route('/v1/group_chat', methods=['POST'])
@flask_login.login_required
def api_group_chat_create():
    new_chat_id = chat_controller.create_group_chat(flask_login.current_user.username)
    return f'{{ "chat_id": {new_chat_id} }}', 200


@app.route('/v1/group_chat/<int:group_chat_id>/participants', methods=['POST'])
@flask_login.login_required
def api_group_chat_add(group_chat_id: int):
    if not chat_controller.is_member(cid=group_chat_id, username=flask_login.current_user.username):
        return 'You are not a member of that chat, so you cannot edit it', 403
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', 400
    try:
        username = data_dict['username']
    except KeyError:
        return 'Malformed request', 400
    try:
        success = chat_controller.add_user_to_chat(group_chat_id, username)
    except ValueError:
        return 'You cannot add members to a P2P chat', 400
    if success:
        return 'Success', 200
    else:
        return 'User is already in that chat', 400


@app.route('/v1/group_chat/<int:group_chat_id>/participants/<string:username>', methods=['DELETE'])
@flask_login.login_required
def api_group_chat_delete(group_chat_id: int, username: str):
    if not chat_controller.is_member(cid=group_chat_id, username=flask_login.current_user.username):
        return 'You are not a member of that chat, so you cannot edit it', 403
    success = chat_controller.delete_user_from_chat(group_chat_id, username)
    if success:
        return 'Success', 200
    else:
        return 'User is not part of that chat', 400


# </editor-fold>
# <editor-fold desc="Messages Routes">
@app.route('/v1/messages', methods=['POST'])
@flask_login.login_required
def api_message_add():
    try:
        data_dict = json.loads(request.data.decode('utf-8'))
    except JSONDecodeError:
        return 'Malformed request', 400
    try:
        # The message is sent to a group chat
        chat_id = data_dict['group_chat_id']
        if not chat_controller.is_member(cid=chat_id,
                                         username=flask_login.current_user.username):
            return 'You are not a member of that chat, so you cannot send messages to it', 403
    except KeyError:
        try:
            # The message is sent to a P2P chat
            dest_username = data_dict['dest_username']
            if not user_controller.exists(dest_username):
                return 'The destination user does no exist', 400
            chat_id = chat_controller.get_p2p_by_members(flask_login.current_user.username,
                                                         dest_username).cid
        except KeyError:
            return 'Malformed request', 400
    message = data_dict['message']
    message_controller.send_message(sender_username=flask_login.current_user.username, cid=chat_id,
                                    message=message)
    return 'Success', 200


@app.route('/v1/messages/group/<int:group_chat_id>', methods=['GET'])
@flask_login.login_required
def api_message_get_group(group_chat_id: int):
    if not chat_controller.is_member(cid=group_chat_id,
                                     username=flask_login.current_user.username):
        return 'You are not a member of that chat, so you cannot view its messages', 403
    message_list = message_controller.get_chat_messages(cid=group_chat_id)
    return json.dumps([str(message) for message in message_list]), 200


@app.route('/v1/messages/p2p/<string:dest_username>', methods=['GET'])
@flask_login.login_required
def api_message_get_p2p(dest_username: str):
    if not user_controller.exists(dest_username):
        return 'The destination user does no exist', 400
    p2p_chat_id = chat_controller.get_p2p_by_members(flask_login.current_user.username,
                                                     dest_username).cid
    message_list = message_controller.get_chat_messages(cid=p2p_chat_id)
    return json.dumps([str(message) for message in message_list]), 200


@app.route('/v1/messages', methods=['GET'])
@flask_login.login_required
def api_messages_get_all():
    message_list = message_controller.get_user_messages(username=flask_login.current_user.username)
    return json.dumps([str(message) for message in message_list]), 200


# </editor-fold>
# </editor-fold>

def startup():
    Repository.create_if_necessary()


if __name__ == 'app':
    startup()
if __name__ == '__main__':
    startup()
    app.run()
