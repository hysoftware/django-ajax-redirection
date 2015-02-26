#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Django Ajax Redirection Middleware
'''

import re

from django.http import HttpResponseRedirect
from django.conf import settings


class AjaxRedirectionMiddleware(object):
    '''
    The middleware
    '''
    # pylint: disable=too-few-public-methods

    def process_request(self, request):
        '''
        Before request wrapper
        '''
        # pylint: disable=no-self-use
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        prefix = (
            getattr(
                settings,
                "AJAX_REDIRECTION_PREFIX",
                None
            ) or "/"
        )

        for static_url in staticfiles_urlpatterns():
            if static_url.resolve(request.get_full_path()[1:]):
                return None

        for black_url_str in getattr(settings, "DISABLE_REDIRECT", []):
            black_url = re.compile(black_url_str)
            if black_url.search(request.get_full_path()[1:]):
                return None

        if not request.is_ajax() and request.get_full_path() != prefix:
            if not prefix.endswith("/"):
                prefix = prefix + "/"
            return HttpResponseRedirect(
                prefix + "#" + request.get_full_path()
            )
