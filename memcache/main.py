from flask import Flask, render_template, url_for, request, send_file, json, jsonify, g
from memcache import webapp

@webapp.route('/')
# returns the main page
def main():
    return 'hi'