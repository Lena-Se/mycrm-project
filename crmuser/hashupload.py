"""
Changing uploading filename
"""
import hashlib
import os
from django.core.files.storage import FileSystemStorage
from mycrm import settings


def hash_upload_to(instance, filename, fieldname):
    """
    Generates new file name based on file data hash
    Args:
        instanse: fileinstance
        filename (str): initial name of file
        fieldname (str): name of field to upload
    Returns:
        (str) new hash-based filename
    """
    ext = os.path.splitext(filename)[1].lower()
    h = hashlib.sha256()
    field = getattr(instance, fieldname)
    for chunk in field.chunks():
        h.update(chunk)
    name = h.hexdigest()

    return os.path.join(
        fieldname,
        name + ext,
    )


def upload_func(inst, filename):
    """
    override standard upload_to method to change filename with hash_upload_to function
    """
    return hash_upload_to(inst, filename, 'user_photo')


class OverwriteStorage(FileSystemStorage):
    """
    Override standard Storage class for non-copying same files
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name