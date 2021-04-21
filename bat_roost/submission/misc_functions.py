import os

def image_name(instance, filename):
    upload_to = 'recipe-images'
    ext = filename.split('.')[-1]
    filename = '{}-img-{}.{}'.format(instance.submission.id, instance.id, ext)
    return os.path.join(upload_to, filename)
