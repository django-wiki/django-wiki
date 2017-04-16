# HOWTO

1. Register an Disqus account in here: https://disqus.com/
2. Sign in and create a site profile: https://disqus.com/admin/create/
3. Add `"wiki.plugins.disqus.context_processors.disqus",` to TEMPLATE_CONTEXT_PROCESSORS in settings.py
4. Configure WIKI_DISQUS_SORTNAME in settings, like this: `WIKI_DISQUS_SORTNAME = "mysite"`