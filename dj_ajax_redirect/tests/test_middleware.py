#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Middleware test specs
'''

import os
import sys

from unittest import TestCase
from django.http import HttpResponseRedirect

from ..tests import TESTS_DIR
from .request_mock import HTTPRequest
from ..middleware import AjaxRedirectionMiddleware


class TestAjaxMode(TestCase):
    '''
    Ajax Mode test case
    '''
    request = None

    def setUp(self):
        '''
        Setup function
        '''
        self.request = HTTPRequest(True, "/test")

    def test_not_redirection(self):
        '''
        The response should be None
        '''
        response = AjaxRedirectionMiddleware().process_request(self.request)
        assert response is None


class TestNonAjaxMode(TestCase):
    '''
    Non-Ajax Mode test case
    '''
    request = None
    path = "/test"

    def setUp(self):
        '''
        Setup function
        '''
        self.request = HTTPRequest(False, self.path)
        sys.path.append(TESTS_DIR)
        os.environ["DJANGO_SETTINGS_MODULE"] = "setting_mock"

    def tearDown(self):
        '''
        Tear Down function
        '''
        sys.path.remove(TESTS_DIR)
        del os.environ["DJANGO_SETTINGS_MODULE"]

    def test_redirection_raw(self):
        '''
        The response should be HttpResponseRedirect prefixed with /#
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", None)
        response = AjaxRedirectionMiddleware().process_request(self.request)
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == "/#" + self.path

    def test_redirection_prefix(self):
        '''
        The response should be HttpResponseRedirect prefixed with /test/#
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", "/test")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        assert isinstance(response, HttpResponseRedirect)
        assert response.url == "/test/#" + self.path
