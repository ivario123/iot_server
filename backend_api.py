from flask import Blueprint, render_template,request
from flask_login import login_required, current_user
from .api import devices, in_list
from .client import *
from . import db
import json


backend_api = Blueprint('backend_api', __name__,url_prefix="/backend")
@backend_api.before_request
def check_login():
  if not current_user.is_authenticated:
    return "Please log in before using this service",401


@backend_api.route('/list',methods = ["GET"])
def index():
    try:
      devices_json = json.dumps(devices,cls=client_encoder)
      return devices_json,200
    except:
      return "Internal server error",500

@backend_api.route('/change',methods = ["POST"])
def change():
    try:
      data = json.loads(request.data)
      name = data["name"]
      state = data["state"]
      index = in_list(name);
      if index == -1:
        return "Not in list",500
      devices[index].state = int(state)
      return "Updated the state",200
    except:
      return "Internal server error",500