import datetime, requests
from flask import Flask, render_template, url_for, request, send_file, json, jsonify, g
from backend.cache_helper import get_cache, set_cache
from backend.database_helper import get_db
from backend.constants import max_capacity, replacement_policy, memcache_host
from backend.image_helper import convert_image_base64, process_image, add_image
from backend.graph_helper import prepare_graph, plot_graph
from backend import webapp

@webapp.before_first_request
def set_cache_config_settings():
    set_cache(max_capacity, replacement_policy)

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@webapp.route('/')
@webapp.route('/home')
# returns the main page
def home():
    return render_template('main.html')

@webapp.route('/keys_list', methods=['GET'])
# returns the webpage list of keys page
def keys_list():
    cnx = get_db()
    cursor = cnx.cursor(buffered=True)
    query = 'SELECT images.key FROM images'
    cursor.execute(query)
    keys = []
    for key in cursor:
        keys.append(key[0])
    cnx.close()

    return render_template('keys_list.html', keys=keys, length=len(keys) )

@webapp.route('/get_image/<string:image>')
# returns the actual image
def get_image(image):
    filepath = 'static/images/' + image
    return send_file(filepath)

@webapp.route('/image', methods = ['GET','POST'])
# returns the view image page
def image():
    if request.method == 'POST':
        key_value = request.form.get('key_value')
        request_json = {
            'key': key_value
        }
        # get the image by key from the memcache
        res = requests.post(memcache_host + '/get_from_memcache', json=request_json)
        if res.text == 'Key Not Found':
            cnx = get_db()
            cursor = cnx.cursor(buffered=True)
            query = 'SELECT images.location FROM images where images.key = %s'
            cursor.execute(query, (key_value,))
            if cursor._rowcount:
                location=str(cursor.fetchone()[0]) 
                cnx.close()
                base64_image = convert_image_base64(location)
                request_json = { 
                    key_value: base64_image 
                }
                # put the key and image into the memcache
                res = requests.post(memcache_host + '/put_into_memcache', json=request_json)
                return render_template('image.html', exists=True, image=base64_image)
            else:
                return render_template('image.html', exists=False, image='does not exist')
        else:
            return render_template('image.html', exists=True, image=res.text)
    return render_template('image.html')

@webapp.route('/upload_image', methods = ['GET','POST'])
# returns the upload page
def upload_image():
    if request.method == 'POST':
        key = request.form.get('key')
        status = process_image(request, key)
        return render_template('upload_image.html', status=status)
    return render_template('upload_image.html')

@webapp.route('/cache_properties', methods = ['GET','POST'])
# returns the cache properties page
def cache_properties():
    cache_properties = get_cache()
    if not cache_properties == None:
        max_capacity = cache_properties[1]
        replacement_policy = cache_properties[2]
        created_at = cache_properties[3]
    else:
        max_capacity = 10
        replacement_policy = 'Least Recently Used'
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        if not request.form.get("clear_cache") == None:
            requests.post(memcache_host + '/clear_cache')
            return render_template('cache_properties.html', max_capacity=max_capacity, replacement_policy=replacement_policy, created_at=created_at, status="CLEAR")
        else: 
            new_max_capacity = request.form.get('max_capacity')
            if new_max_capacity.isdigit() and int(new_max_capacity) <= 2000:
                new_replacement_policy = request.form.get('replacement_policy')
                created_at = set_cache(new_max_capacity, new_replacement_policy)
                if not created_at == None:
                    new_created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    response = requests.post(memcache_host + '/refresh_configuration')
                    if response.json() == 'OK':
                        return render_template('cache_properties.html', max_capacity=new_max_capacity, replacement_policy=new_replacement_policy, created_at=new_created_at, status="OK")
            return render_template('cache_properties.html', max_capacity=max_capacity, replacement_policy=replacement_policy, created_at=created_at, status="INVALID")
    return render_template('cache_properties.html', max_capacity=max_capacity, replacement_policy=replacement_policy, created_at=created_at)

@webapp.route('/cache_stats', methods = ['GET','POST'])
# returns the cache stats page
def cache_stats():
    cnx = get_db()
    cursor = cnx.cursor(dictionary=True)
    stop_time = datetime.datetime.now()
    start_time = stop_time - datetime.timedelta(minutes=10)
    query = '''SELECT * FROM cache_stats WHERE cache_stats.created_at > %s and cache_stats.created_at < %s'''
    cursor.execute(query, (start_time, stop_time,))
    data = cursor.fetchall()
    cnx.close()

    (x_data, y_data) = prepare_graph(data)
    
    graph_image = {}
    for key, value in y_data.items():
        graph_image[key] = plot_graph(x_data['x-axis'], value, key)
    return render_template('cache_stats.html', cache_count_graph = graph_image['cache_count'], 
                            request_count_graph = graph_image['request_count'], cache_size_graph = graph_image['cache_size'], 
                             hit_graph = graph_image['hit_count'], miss_graph = graph_image['miss_count'])

@webapp.route('/api/list_keys', methods=['POST'])
def list_keys():
    try:
        cnx = get_db()
        cursor = cnx.cursor()
        query = 'SELECT images.key FROM images'
        cursor.execute(query)
        keys = []
        for key in cursor:
            keys.append(key[0])
        cnx.close()

        response = {
          'success': 'true',
          'keys': keys
        }
        return jsonify(response)

    except Exception as e:
        error_response = {
            'success': 'false',
            'error': {
                'code': '500 Internal Server Error',
                'message': 'Unable to fetch a list of keys, something went wrong.' + e
                }
            }
        return(jsonify(error_response))

@webapp.route('/api/key/<string:key_value>', methods=['POST'])
def key(key_value):
    try:        
        request_json = {
            'key': key_value
        }
        # get the image by key from the memcache
        res = requests.post(memcache_host + '/get_from_memcache', json=request_json)
        if res.text == 'Key Not Found':
            cnx = get_db()
            cursor = cnx.cursor(buffered=True)
            query = 'SELECT images.location FROM images where images.key = %s'
            cursor.execute(query, (key_value,))
            if cursor._rowcount:
                location=str(cursor.fetchone()[0]) 
                cnx.close()
                base64_image = convert_image_base64(location)
                request_json = { 
                    key_value: base64_image 
                }
                # put the key and image into the memcache
                res = requests.post(memcache_host + '/put_into_memcache', json=request_json)
                response = {
                    'success': 'true' , 
                    'content': base64_image
                }
                return jsonify(response)
            else:
                response = {
                    'success': 'false', 
                    'error': {
                        'code': '406 Not Acceptable', 
                        'message': 'The associated key does not exist'
                        }
                    }
                return jsonify(response)
        else:
            response = {
                'success': 'true' , 
                'content': res.text
            }   
            return jsonify(response)
    except Exception as e:
        error_response = {
            'success': 'false',
            'error': {
                'code': '500 Internal Server Error', 
                'message': 'Unable to fetch the associated key, something went wrong.' + e
                }
            }
        return(jsonify(error_response))

@webapp.route('/api/upload', methods = ['POST'])
def upload():
    try:
        key = request.form.get('key')
        status = add_image(request, key)
        if status == 'INVALID' or status == 'FAILURE':
            error_response = {
                'success': 'false', 
                'error' : {
                    'code': '500 Internal Server Error', 
                    'message': 'Unable to upload image, something went wrong.'
                }
            }
            return jsonify(error_response)
        response = {
            'success': 'true'
        }
        return jsonify(response)

    except Exception as e:
        error_response = {
            'success': 'false',
            'error': {
                'code': '500 Internal Server Error', 
                'message': 'Unable to upload image something went wrong.' + e
                }
            }
        return(jsonify(error_response))

@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@webapp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500