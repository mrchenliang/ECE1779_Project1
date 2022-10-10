from backend.cache_config import set_cache
from flask import Flask, render_template, url_for, request, json, jsonify
from backend.database_config import get_db
from backend.constants import max_capacity, replacement_policy
from backend import webapp, memcache


@webapp.before_first_request
def set_cache_db_settings():
    set_cache(max_capacity, replacement_policy)

@webapp.route('/')
@webapp.route('/home')
# returns the main page
def main():
    return render_template("main.html")

@webapp.route('/keys_list', methods=['GET'])
# returns the webpage list of keys
def keys_list():
    cnx = get_db()
    cursor = cnx.cursor(buffered=True)
    query = "SELECT images.key FROM images"
    cursor.execute(query)
    keys = []
    for key in cursor:
        keys.append(key[0])
    cnx.close()

    return render_template("keys_list.html", keys=keys, length=len(keys_list) )

@webapp.route('/image', methods = ['GET','POST'])
# returns the view image page
def image():
    return render_template("image.html")

@webapp.route('/upload')
# returns the upload page
def upload():
    return render_template("upload.html")

# @webapp.route('/api/get', methods=['POST', 'GET'])
# def get():
#     key = request.form.get('key')
#     if key in memcache:
#         value = memcache[key]
#         response = webapp.response_class(
#             response=json.dumps(value),
#             status=200,
#             mimetype='application/json'
#         )
#     else:
#         response = webapp.response_class(
#             response=json.dumps("Unknown key"),
#             status=400,
#             mimetype='application/json'
#         )
#     if key == '1':
#         return render_template("image.html", content='1234', extension='4321')

#     return response

# @webapp.route('/api/put', methods=['POST'])
# def put():
#     key = request.form.get('key')
#     value = request.form.get('value')
#     memcache[key] = value

#     response = webapp.response_class(
#         response=json.dumps("OK"),
#         status=200,
#         mimetype='application/json'
#     )

#     return response

@webapp.route('/api/list_keys', methods=['POST'])
def list_keys():
    try:
        cnx = get_db()
        cursor = cnx.cursor()
        query = "SELECT images.key FROM images"
        cursor.execute(query)
        keys = []
        for key in cursor:
            keys.append(key[0])
        cnx.close()

        data = {
            'success': 'true',
            'keys': keys
        }
        return jsonify(data)

    except Exception as e:
        error = {
            'success': 'false',
            'error': {
                'code': '500',
                'message': 'Unable to fetch a list of keys, something went wrong'
                }
            }
        return(jsonify(error))

@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@webapp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500