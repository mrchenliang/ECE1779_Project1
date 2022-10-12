import base64, os
from backend import IMAGE_FOLDER
from backend.constants import ALLOWED_EXTENSIONS
from backend.database_helper import get_db

def convert_image_base64(fp):
    with open(IMAGE_FOLDER + '/' + fp, 'rb') as image:
        base64_image = base64.b64encode(image.read())
    base64_image = base64_image.decode('utf-8')
    return base64_image

def process_image(request, key):
      file = request.files['file']
      _, extension = os.path.splitext(file.filename)

      if extension.lower() in ALLOWED_EXTENSIONS:
            filename = key + extension
            file.save(os.path.join(IMAGE_FOLDER, filename))
            # implement memcache (post request for invalidate image)
            return add_image_to_db(key, filename)
      return 'INVALID'

def add_image_to_db(key, location):
    if key == '' or location == '':
        return 'FAILURE'
    try:
        cnx = get_db()
        cursor = cnx.cursor(buffered = True)
        query_exists = 'SELECT EXISTS(SELECT 1 FROM images WHERE images.key = (%s))'
        cursor.execute(query_exists,(key,))
        for elem in cursor:
            if elem[0] == 1:
                query_delete = 'DELETE FROM images WHERE images.key=%s'
                cursor.execute(query_delete,(key,))
                break
        query_insert = '''INSERT INTO images (images.key, images.location) VALUES (%s,%s);'''
        cursor.execute(query_insert,(key,location,))
        cnx.commit()
        cnx.close()
        return 'OK'
    except:
        return 'FAILURE'

def add_image(request, key):
    try:
        file = request.files['file']
        _, extension = os.path.splitext(file.filename)

        if extension.lower() in ALLOWED_EXTENSIONS:
            filename = key + extension
            file.save(os.path.join(IMAGE_FOLDER, filename))
            # implement memcache (post request for invalidate image)
            return add_image_to_db(key, filename)
        return 'INVALID'
    except:
        return "INVALID"