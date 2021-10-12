from os import name
from flask import Blueprint, sessions
from flask import request as Request
from flask_login.utils import login_required
from sqlalchemy.orm import session
from .client import *
from .switch import switch
from . import app


# The api Blueprint
api = Blueprint('api', __name__,url_prefix="/api")


device_types = {
    "switch":  switch,    # The switch class,
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

def valid_key (form):
    import os
    script_dir = os.path.dirname(__file__)
    f = open(os.path.join(script_dir, "./.data/api.key"), 'r')
    API_KEY = f.read()
    if form.get("key") != API_KEY:
        return -1
    return 0

@api.route('/append', methods=["POST"])
def append():
    if 0!=valid_key(Request.form):
      return "invalid API key",401
    session["valid"] = True
    name = Request.form.get("name")
    index = in_list(name)
    if(index != -1):
        devices[index].active = True
        devices[index].state = Request.form.get("state")
        return "back so soon?",200
    try:
      device = device_types[Request.form.get("type")]
    except:
      device = device_types[""] 

    methods = Request.form.get("methods")
    state = Request.form.get("state")
    devices.append(device(name, device, methods, state))

    return f"Registered a new device {name}",200


@api.route("/read", methods=["GET"])
def read():
    try:
      if not session["valid"]:
          return "invalid API key",401
    except:
          return "invalid API key",401
    name = Request.form.get("name")
    index = in_list(name)

    if (index == -1):
      return "Not registerd",500
    devices[index].active = True
    
    return f"{devices[index].state}",200

@api.route("/get/devices",methods = ["GET"])
def get_devices():
    try:
      if not session["valid"]:
          return "invalid API key",401
    except:
          return "invalid API key",401
    try:
      devices_json = json.dumps(devices,cls=client_encoder)
      return devices_json,200
    except:
      return "Internal server error",500


@api.route("/change/state",methods = ["POST"])
def change_state():
    try:
      if not session["valid"]:
          return "invalid API key",401
    except:
          return "invalid API key",401

    index = in_list(Request.form.get("name"))
    if -1 == index:
      return "Device not registered",500
    state = Request.form.get("state")
    if state:
      devices[index].state = state
    else:
      return "Internal server error",500
    
    return f"New state = {state}",200
  

@api.route("/remove/client",methods = ["POST"])
def remove_client():
    try:
      if not session["valid"]:
          return "invalid API key",401
    except:
          return "invalid API key",401

    index = in_list(Request.form.get("name"))
    if -1 == index:
      return "Device not registered",500
    
    try:
      devices.remove(devices[index])
    except:
      return "Internal server error",500
    
    return f"Removed the device {name}",200