import os
import mimetypes
from datetime import datetime

from django.http import HttpResponse
from django.utils.http import http_date
from django.utils import dateformat

def send_file(request, filepath, last_modified=None, filename=None):
    fullpath = filepath
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    if filename:
        mimetype, encoding = mimetypes.guess_type(filename)
    else:
        mimetype, encoding = mimetypes.guess_type(fullpath)
        
    mimetype = mimetype or 'application/octet-stream'
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
        response["Content-Disposition"] = "attachment; filename=%s" % filename.encode('utf-8')
    
    return response
