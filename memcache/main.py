from flask import Flask, render_template, url_for, request, send_file, json, jsonify, g
from memcache import webapp
from memcache.response_helper import response_builder
from backend.cache_helper import get_cache
from memcache_operator import *
from memcache import scheduler


@webapp.route('/put_into_memcache', methods=['GET', 'POST'])
def put_memcache(key, file):
    flag = put_into_memcache(key, file)
    return response_builder(flag)


@webapp.route('/get_from_memcache', methods=['GET', 'POST'])
def get_memcache(key):
    file = get_from_memcache(key)
    if file is None:
        return "Miss"
    else:
        return file


@webapp.route('/clear_cache', methods=['GET', 'POST'])
# clears the memcache object
def clear_cache():
    flag = clear_all_from_memcache()
    return response_builder(flag)


@webapp.route('/refresh_configuration', methods=['GET', 'POST'])
# refresh the memcache configuration
def refresh_configuration():
    flag = refresh_config_of_memcache()
    scheduler.add_job(id="update_memcache_statistics", func=store_statistic_into_db,
                      trigger="interval", seconds=5)
    return response_builder(flag)


@webapp.route('/invalidate_specific_key', methods=['GET', 'POST'])
def invalidate_key(key):
    flag = invalidate_specific_key(key)
    return response_builder(flag)
