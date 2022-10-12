from flask import Flask, render_template, url_for, request, send_file, json, jsonify, g
from memcache import webapp
from memcache.response_helper import response_builder
from backend.cache_helper import get_cache, set_cache

@webapp.route('/clear_cache', methods = ['GET', 'POST'])
# clears the memcache object
def clear_cache():
    memcache_object = {}
    return response_builder(True)

@webapp.route('/refresh_configuration', methods = ['POST'])
# refresh the memcache configuration
def refresh_configuration():
    cache_properties = get_cache()
    if not cache_properties == None:
        max_capacity = cache_properties[1]
        replacement_policy = cache_properties[2]
        set_cache(max_capacity, replacement_policy)
        # implement setting up new memcache
        return response_builder(True)
    return None