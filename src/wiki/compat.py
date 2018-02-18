try:
    from django.urls import include, re_path as url
except ImportError:
    from django.conf.urls import include, url


__all__ = [
    'include', 'url'
]
