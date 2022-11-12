import math
import threading
import time
import base64
import http.client
from re import TEMPLATE
import requests
import mysql.connector
from flask import json, render_template, url_for, request, g, flash, redirect, send_file, jsonify
import boto3
from botocore.exceptions import ClientError

# custom imports
import managerapp
from managerapp import webapp
from managerapp.config import ConfigManager
# from managerapp.showchart import Chart
import tools
from tools.awsS3 import S3_Class
from tools.awsEC2 import MemcacheEC2
from tools.awsCloudwatch import CloudwatchAPI
from tools.credential import ConfigAWS
import urllib.request


import os
TEMPLATE_DIR = os.path.abspath("./templates")
STATIC_DIR = os.path.abspath("./static")

# Mode config for autoscaler. 0 = manual mode, 1 = auto mode.
AUTOSCALER_MODE = 1
CAPACITY_B = 1048576
REPLACE_POLICY = 1


def connect_to_database():
    return mysql.connector.connect(user=ConfigManager.db_config['user'],
                                   password=ConfigManager.db_config['password'],
                                   host=ConfigManager.db_config['host'],
                                   database=ConfigManager.db_config['database'])


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
