#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Django Ajax Redirection Middleware
'''

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
        if not request.is_ajax():
            return HttpResponseRedirect(
                (getattr(
                    settings,
                    "AJAX_REDIRECTION_PREFIX",
                    None
                ) or "") + "/#" + request.get_full_path()
            )