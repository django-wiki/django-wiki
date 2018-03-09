Disqus comment embed
====================

This page describes how to embed the Disqus_ comment system on each wiki page.

Put the following as ``wiki/base.html`` somewhere in your
``TEMPLATE_DIRS``:

..  code-block:: html+django

    {% extends "wiki/base_site.html" %}
    {% load sekizai_tags %}

    {% block wiki_body %}
      {{ block.super }}
      {% block wiki_footer_logo %}
      {% endblock wiki_footer_logo %}
      {% if selected_tab == 'view' %}
        {% addtoblock "js" %}
        <script type="text/javascript">
        (function(){
          $("#wiki-footer p").eq(0).after('<div id="disqus_thread"></div>')
        })();
        var disqus_shortname = 'your_disqus_shortname';
        (function() {
          var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
          dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
          (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
        </script>
        {% endaddtoblock %}
      {% endif %}
    {% endblock wiki_body %}

Replace ``your_disqus_sortname`` with your disqus sortname.

See also in :doc:`/customization`.

.. _Disqus: https://disqus.com/
