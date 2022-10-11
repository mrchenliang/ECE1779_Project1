import base64
from backend import IMAGE_FOLDER


def convert_image_base64(fp):
    with open(IMAGE_FOLDER + "/" + fp, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read())
    base64_image = base64_image.decode('utf-8')
    return base64_image