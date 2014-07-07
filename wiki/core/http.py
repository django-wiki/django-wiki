from __future__ import unicode_literals
import os
import mimetypes
from datetime import datetime
import six

from django.http import HttpResponse
from django.utils.http import http_date
from django.utils import dateformat

from wiki.conf import settings

def django_sendfile_response(request, filepath):
    from sendfile import sendfile
    return sendfile(request, filepath)


def send_file(request, filepath, last_modified=None, filename=None):
    fullpath = filepath
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    if filename:
        mimetype, encoding = mimetypes.guess_type(filename)
    else:
        mimetype, encoding = mimetypes.guess_type(fullpath)
        
    mimetype = mimetype or 'application/octet-stream'
    
    if settings.USE_SENDFILE:
        response = django_sendfile_response(request, filepath)
    else:
        response = HttpResponse(open(fullpath, 'rb').read(), mimetype=mimetype)
    
    if not last_modified:
        response["Last-Modified"] = http_date(statobj.st_mtime)
    else:
        if isinstance(last_modified, datetime):
            last_modified = float(dateformat.format(last_modified, 'U'))
        response["Last-Modified"] = http_date(epoch_seconds=last_modified)
    
    response["Content-Length"] = statobj.st_size
    
    if encoding:
        response["Content-Encoding"] = encoding
    
    # TODO: Escape filename
    if filename:
        print(filename, type(filename))
        if six.PY2:
            response["Content-Disposition"] = "attachment; filename=%s" % filename.encode('utf-8')
        else:
            #filename is already an unicode string
            response["Content-Disposition"] = "attachment; filename=%s" % filename
    
    return response
