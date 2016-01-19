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

### Note

1. Template doesn't support mixed markdown and html
2. If you want use html content in template, you must configure the settings of WIKI_MARKDOWN_KWARGS options. Turn 'safe_mode' off.

```
WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'codehilite',
        'footnotes',
        'attr_list',
        'headerid',
        'extra',
    ], "safe_mode": False,}
```