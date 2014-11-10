## Variables, Templates

django-wiki implementation of the MediaWiki template language.

### Usage

This is your article

```
## Hello {{world|name=Earth}}!

{{outlink
|django-wiki
|https://github.com/django-wiki/django-wiki
}}
```

A template named 'world'

```
world **{{{name}}}**
```

A template named 'outlink'

```
<a href="{{{1}}}" target="_blank">{{{0}}} <i class="icon icon-share"></i></a>
```

Finally article:

```
## Hello world **Earth**!

<a href="https://github.com/django-wiki/django-wiki" target="_blank">django-wiki <i class="icon icon-share"></i></a>
```

