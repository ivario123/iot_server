from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .api import *
from .client import *
from . import db
import json


def get_user_devices(session, devices_list):
    user_devices = []
    for device in devices_list:
        # Check if the user is allowed to view that device, and check if the device has an owner
        if device.correct_owner(session["user_id"]) or device.correct_owner(None):
            user_devices.append(device)
    print(len(user_devices))
    return user_devices


backend_api = Blueprint('backend_api', __name__, url_prefix="/backend")


@backend_api.before_request
def check_login():
    if not current_user.is_authenticated:
        return render_template(
            'error.html', error="Please log in before using this service"), 401


@backend_api.route('/dict', methods=["GET"])
def dict():
    return encode(get_dictionary(get_user_devices(session,devices)))


@backend_api.route('/list', methods=["GET"])
def list():
    try:
        user_devices = get_user_devices(session, devices)
        devices_json = encode(user_devices)
        return devices_json, 200
    except Exception as inst:
        print(inst)
        return render_template('error.html', error="Internal server error"), 500


@backend_api.route('/change', methods=["POST"])
def change():
    try:
        data = json.loads(request.data)
        name = data["name"]
        state = data["state"]
        print(session.__str__())
        user_id = session["user_id"]
        index = in_list(name, user_id)
        if index == -1:
            return render_template('error.html', error="not in list"), 500
        devices[index].state = int(state)
        return "Updated the state", 200
    except:
        return render_template('error.html', error="Internal server error"), 500
