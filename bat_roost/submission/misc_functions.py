import os
from uuid import uuid4

def image_name(instance, filename):
    upload_to = 'submission-images'
    ext = filename.split('.')[-1]
    filename = '{}-img-{}.{}'.format(instance.submission.pk, uuid4(), ext)
    return os.path.join(upload_to, filename)
