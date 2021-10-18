from os import name
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login.utils import login_required
from .client import *
from .switch import switch
from .dimmer import dimmer
from . import app
import difflib

# The api Blueprint
api = Blueprint('api', __name__, url_prefix="/api")


device_types = {
    "switch":  switch,    # The switch class,
    "dimmer":  dimmer,    # The dimmer class,
    "client": client,     # The base class for clients
    "": client            # ...
}
devices = []


def check_active():
    for dev in devices[::-1]:
        if dev.active != True:
            devices.remove(dev)
        else:
            dev.active = False


def in_list(name: str):
    itter = 0
    for dev in devices:
        if dev.name == name:
            return itter
        itter += 1
    return -1

def valid_key(key: str):
    import os
    script_dir = os.path.dirname(__file__)
    f = open(os.path.join(script_dir, "./.data/api.key"), 'r')
    API_KEY = f.read()
    if key != API_KEY:
        return -1
    return 0


@api.route('/append', methods=["POST"])
def append():
        data = json.loads(request.data)
        user_key = data["key"]
        user_name = data["name"]
        if valid_key(user_key):
            return "invalid API key", 401
        index = in_list(user_name)
        if(index != -1):
            devices[index].active = True
            return "back so soon?", 200
        try:
            device = device_types[data["type"]]
        except:
            device = device_types[""]
        devices.append(device(user_name, device))

        return f"Registered a new device {name}", 200


@api.route("/read/<device>/<api>", methods=["GET"])
def read(device,api):
    if valid_key(api):
            return "invalid API key", 401
    index = in_list(device)

    if (index == -1):
        return "Not registerd", 500
    devices[index].active = True

    return f"{devices[index].state}", 200


@api.route("/get/devices/<api_key>", methods=["GET"])
def get_devices(api_key):
    try:
        if valid_key(api_key):
            return "invalid API key", 401
    except:
        return "invalid API key", 401
    try:
        devices_json = json.dumps(devices, cls=client_encoder)
        return devices_json, 200
    except:
        return "Internal server error", 500


@api.route("/change/state", methods=["POST"])
def change_state():
    try:
        if not session["valid"]:
            return "invalid API key", 401
    except:
        return "invalid API key", 401

    index = in_list(request.form.get("name"))
    if -1 == index:
        return "Device not registered", 500
    state = request.form.get("state")
    if state:
        devices[index].change_state(state)
    else:
        return "Internal server error", 500

    return f"New state = {state}", 200


@api.route("/remove/client", methods=["POST"])
def remove_client():
    try:
        if not session["valid"]:
            return "invalid API key", 401
    except:
        return "invalid API key", 401

    index = in_list(request.form.get("name"))
    if -1 == index:
        return "Device not registered", 500

    try:
        devices.remove(devices[index])
    except:
        return "Internal server error", 500

    return f"Removed the device {name}", 200
