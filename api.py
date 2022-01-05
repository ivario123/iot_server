import json
from os import name
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login.utils import login_required
from .client import *
from . import app

import difflib

# The api Blueprint
api = Blueprint('api', __name__, url_prefix="/api")


devices = []


def get_dictionary(el_list):
    """
    Returns a dictionary with the clients sorted by type
    """
    organised_list = {}
    for el in el_list:

        if el.type not in organised_list.keys():
            organised_list[el.type] = [el]
        else:
            organised_list[el.type].append(el)
    return organised_list


def check_active():
    """
        Checks if a device has past it's lifetime

        if it has, it removes it
        @return none

    """
    for dev in devices[::-1]:
        if dev.active != True:
            devices.remove(dev)
        else:
            dev.active = False


def in_list(name: str, owner: str = None):
    """
        Checks if a device with that name is registered
        @parameters name the name of the device you want to check
        @return index if in list else 0
    """
    itter = 0
    for dev in devices:
        if dev.name == name and dev.owner == owner:
            return itter
        itter += 1
    # Rerun check to see if the device has None owner
    if owner == None:
        return -1
    # Rerun check to see if the device has None owner
    itter = 0
    for dev in devices:
        if dev.name == name and dev.owner == None:
            return itter
        itter += 1
    return -1


def valid_key(key: str):
    """
        Checks if an api key is valid.
        @returns 0 if valid else -1
    """
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
    try:
        owner = data["owner"]
    except:
        owner = None
    #print(f"Register request from : name :{user_name} , owner : {owner}")
    if valid_key(user_key):
        return "invalid API key", 401

    try:
        device = device_types[data["type"]]
    except:
        device = device_types[""]

    index = in_list(user_name, owner)
    if(index != -1):
        if("sensor" in data["type"]):
            devices[index].state = data["state"]
        devices[index].active = True
        return "back so soon?", 200

    devices.append(device(user_name, device,owner=owner))

    return f"Registered a new device {name}", 200


@api.route("/read/<device>/<api>", methods=["GET"])
def read(device, api):
    """
    Depreciated, use the owner api
    """
    if valid_key(api):
        return "invalid API key", 401
    index = in_list(device, None)

    if (index == -1):
        return "Not registerd", 500
    devices[index].active = True

    return f"{devices[index].state}", 200


@api.route("/read/<owner>/<device>/<api_key>", methods=["GET"])
def read_with_owner(device, api_key, owner):
    if valid_key(api_key):
        return "invalid API key", 401
    index = in_list(device, owner)

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

        devices_json = encode(devices)
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

    try:
        data = json.loads(request.data)
    except:
        data = request.form.to_dict()
    try:
        index = in_list(data["name"], data["owner"])
    except:
        index = in_list(data["name"])
    if -1 == index:
        return "Device not registered", 500
    state = data["state"]
    if state:
        devices[index].change_state(state)
    else:
        return "Internal server error", 500

    return f"New state = {state}", 200


@api.route("/remove/client", methods=["POST"])
def remove_client():
    try:
        data = json.loads(request.data)
    except:
        data = request.form.to_dict()
    try:
        if not session["valid"]:
            return "invalid API key", 401
    except:
        return "invalid API key", 401

    try:
        index = in_list(data["name"], data["owner"])
    except:
        index = in_list(data["name"])
    if -1 == index:
        return "Device not registered", 500

    try:
        devices.remove(devices[index])
    except:
        return "Internal server error", 500

    return f"Removed the device {name}", 200
