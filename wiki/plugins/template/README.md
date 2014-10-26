## Variables, Templates

django-wiki implementation of the MediaWiki template language.

### Usage

```
The article

## Hello {{world|name=Earth}}!

--------------

The template named 'world'

world **{{{name}}}**

--------------

Finally article

## Hello world **Earth**!

```