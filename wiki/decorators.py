from django.utils import simplejson as json
from django.http import HttpResponse
def json_view(func):
    def wrap(request, *a, **kw):
        obj = func(request, *a, **kw)
        data = json.dumps(obj, ensure_ascii=False)
        response = HttpResponse(mimetype='application/json')
        response.write(data)
        return response
    return wrap