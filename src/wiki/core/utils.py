from django.http.response import JsonResponse


def object_to_json_response(obj, status=200):
    """
    Given an object, returns an HttpResponse object with a JSON serialized
    version of that object
    """
    return JsonResponse(
        data=obj, status=status, safe=False, json_dumps_params={'ensure_ascii': False},
    )
