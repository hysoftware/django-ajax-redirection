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
        sys.path.append(TESTS_DIR)
        os.environ["DJANGO_SETTINGS_MODULE"] = "setting_mock"
        self.request = HTTPRequest(True, "/test")
    def tearDown(self):
        '''
        Tear Down function
        '''
        sys.path.remove(TESTS_DIR)
        del os.environ["DJANGO_SETTINGS_MODULE"]

    def test_not_redirection(self):
        '''
        The response should be None
        '''
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response, "Response should be None")


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
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "Response should be an instance of HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#" + self.path,
            "The redirect destination should be prefixed with /#/"
        )

    def test_redirection_prefix(self):
        '''
        The response should be HttpResponseRedirect prefixed with /test/#
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", "/test_prefix")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "The response should be HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/test_prefix/#" + self.path,
            "The path should be prefixed with /test_prefix/#"
        )

    def test_root_not_redirect(self):
        '''
        The response shouldn't redirect when accessing root directory.
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", None)
        self.request = HTTPRequest(False, "/")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response, "Response should be None")

    def test_prefix_not_redirect(self):
        '''
        The response shouldn't redirect when accessing root directory.
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", "/test")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response, "Response should be None")
