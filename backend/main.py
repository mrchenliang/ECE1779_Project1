from flask import Flask, render_template, url_for, request, json, jsonify
from backend import webapp, memcache

@webapp.route('/')
@webapp.route('/home')
# returns the main page
def main():
    return render_template("main.html")

@webapp.route('/list')
# returns the list of keys and paths in the database
def list():
    keylist = [
        {'key': 1, 'path': '1234'},
        {'key': 2, 'path': '4321'},
    ]
    view = render_template("list.html", list =keylist)
    return view

@webapp.route('/image' methods = ['GET','POST'])
# returns the view image page
def image():
    return render_template("image.html")

@webapp.route('/upload')
# returns the upload page
def upload():
    return render_template("upload.html")

@webapp.route('/api/get', methods=['POST', 'GET'])
def get():
    key = request.form.get('key')
    if key in memcache:
        value = memcache[key]
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )
    if key == '1':
        return render_template("image.html", content='1234', extension='4321')

    return response

@webapp.route('/api/put', methods=['POST'])
def put():
    key = request.form.get('key')
    value = request.form.get('value')
    memcache[key] = value

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response

@webapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@webapp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500