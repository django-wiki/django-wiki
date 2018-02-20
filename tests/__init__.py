def hacks():
    from django.test import testcases
    if not hasattr(testcases, "WSGIServer"):
        # django-functest: patch django until is released a new version with
        # https://github.com/django-functest/django-functest/pull/14 merged
        from django.core.servers.basehttp import WSGIServer
        testcases.WSGIServer = WSGIServer


hacks()
