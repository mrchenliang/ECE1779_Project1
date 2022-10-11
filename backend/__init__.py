from flask import Flask
import os


global memcache
global IMAGE_FOLDER

webapp = Flask(__name__)
memcache = {}
IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/images'


from backend import main




