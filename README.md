Overview
========

fuzzitusbackend is a Django Tastypie based RESTFul backend for the
fuzzit.us Beacon game. Currently it requires the following Python
packages:

* django
* tastypie
* tastypie-swagger: api doc generator
* pipeline: css and js asset manager for django
* bootstrapform: use bootstrap-style-css in django forms

Endpoint URLs
=========

* /api/v1/ Root Endpoint URL that lists all the endpoints in this api.
* /api/doc/ Documentation Endpoint URL that shows a list of endpoints
  available in this api.
* /admin/ Django admin site.
* /admin/doc/ Django admin site doc.

