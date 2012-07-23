from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url('^$', 'wiki.views.index', name='index'),   
)

def get_pattern(app_name="wiki", namespace="wiki"):
    """Every url resolution takes place as "wiki:view_name".
       You should not attempt to have multiple deployments of the wiki on
       one site.
       https://docs.djangoproject.com/en/dev/topics/http/urls/#topics-http-reversing-url-namespaces
    """
    return urlpatterns, app_name, namespace