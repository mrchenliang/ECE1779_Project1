from flask import Flask
import datetime

from managerapp.config import ConfigManager

webapp = Flask(__name__)

try:
    from managerapp import main

except Exception as e:
    print("No Manager App?")
    print("Error: ", e)
