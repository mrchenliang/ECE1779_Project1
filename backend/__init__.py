from flask import Flask
import os

from flask import Flask
from backend import main

global IMAGE_FOLDER

webapp = Flask(__name__)

IMAGE_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/static/images'
