from flask import make_response


def get_image_response(image_binary, image_name):
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='%s.jpg' % image_name)
    return response