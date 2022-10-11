from flask import Flask, render_template, url_for, request, send_file, json, jsonify, g
from memcache import webapp
from memcache.response_helper import response_builder

@webapp.route('/clear_cache', methods = ['GET', 'POST'])
# clears the memcache object
def clear_cache():
    memcache_object = {}
    return response_builder(True)