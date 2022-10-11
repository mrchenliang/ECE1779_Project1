import base64, os
from backend.constants import ALLOWED_EXTENSIONS
from backend import IMAGE_FOLDER
from backend.database_config import get_db

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
          return write_img_db(key, filename)
      return 'INVALID'

def write_img_db(key, location):
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