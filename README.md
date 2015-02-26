# Ajax redirection middleware for Django

[![Build Status](https://travis-ci.org/hysoftware/django-ajax-redirection.svg)](https://travis-ci.org/hysoftware/django-ajax-redirection)
[![Code Health](https://landscape.io/github/hysoftware/django-ajax-redirection/master/landscape.svg?style=flat)](https://landscape.io/github/hysoftware/django-ajax-redirection/master)

## What this?
This is a collection of useful middlware for Django with Ajax.
For example, [AngularJS](https://angularjs.org/) has URL routing subsystem,
which uses AJAX. In addition, it supports history push state. This mean, when
you access the website with ```https://example.com/#/login```, the addressbar
shows ```https://example.com/login```. However, accessing
```https://example.com/login```, you will get 404, because the HTTP request
is sent to ```https://example.com/login```, not ```https://example.com/#/login```.
To avoid this problem, we should redirect the route to
```https://example.com/#/login```, when accessing ```https://example.com/login```.

This module provides middleware to avoid the problem.

## How to use
### Middleware
1. Add ```dj_ajax_redirect.middleware.AjaxRedirectionMiddleware```
to ```MIDDLEWARE_CLASSES``` on your setting.

## Disable redirection
### Middleware
Just add a new item named "DISABLE_REDIRECT", of which type is list. i.e. just like this:

~~~~
DISABLE_REDIRECT = [
    r"^path_to_disable_redirect/disable$"
]
~~~~

Note that static files are already added to disable list. Therefore, you don't need to add
static urls.

In addition, *the strings are treated as regexp-s*.
