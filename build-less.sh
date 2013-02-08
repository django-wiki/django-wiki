#!/bin/sh

lessc wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less wiki/static/wiki/bootstrap/css/wiki-bootstrap.css
lessc -x wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap.less wiki/static/wiki/bootstrap/css/wiki-bootstrap.min.css

lessc wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap-responsive.less wiki/static/wiki/bootstrap/css/wiki-bootstrap-responsive.css
lessc -x wiki/static/wiki/bootstrap/less/wiki/wiki-bootstrap-responsive.less wiki/static/wiki/bootstrap/css/wiki-bootstrap-responsive.min.css
