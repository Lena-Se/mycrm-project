import hashlib
import os

from django.core.files.storage import FileSystemStorage

from mycrm import settings


def hash_upload_to(instance, filename, fieldname):
    ext = os.path.splitext(filename)[1].lower()
    class_name = instance.__class__.__name__.lower()

    h = hashlib.sha256()
    field = getattr(instance, fieldname)
    for chunk in field.chunks():
        h.update(chunk)
    name = h.hexdigest()

    return os.path.join(
        fieldname,
        name + ext,
    )


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name