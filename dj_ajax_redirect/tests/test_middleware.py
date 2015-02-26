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
from django.test.utils import setup_test_environment
sys.path.append(TESTS_DIR)
os.environ["DJANGO_SETTINGS_MODULE"] = "setting_mock"
setup_test_environment()


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

    def tearDown(self):
        from django.conf import settings
        if hasattr(settings, "AJAX_REDIRECTION_PREFIX"):
            delattr(settings, "AJAX_REDIRECTION_PREFIX")
        if hasattr(settings, "DISABLE_REDIRECT"):
            delattr(settings, "DISABLE_REDIRECT")

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

    def test_child_redirection_raw(self):
        '''
        The response should be HttpResponseRedirect prefixed with /#
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", None)
        self.request = HTTPRequest(False, self.path + "/test2")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "Response should be an instance of HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#" + self.path + "/test2",
            "The redirect destination should be prefixed with /#/"
        )

    def test_redirection_prefix(self):
        '''
        The response should be HttpResponseRedirect
        prefixed with /test_prefix/#
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

    def test_child_redirection_prefix(self):
        '''
        The response should be HttpResponseRedirect
        prefixed with /test_prefix/#
        '''
        from django.conf import settings
        setattr(settings, "AJAX_REDIRECTION_PREFIX", "/test_prefix")
        self.request = HTTPRequest(False, self.path + "/test2")
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "Response should be an instance of HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/test_prefix/#" + self.path + "/test2",
            "The redirect destination should be prefixed with /#/"
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

    def test_static_file_root(self):
        '''
        The response shouldn't redirect when accessing static file of /.
        '''
        from django.conf import settings
        static_path = getattr(settings, "STATIC_URL", None)
        self.assertIsNotNone(static_path)

        self.request = HTTPRequest(
            False,
            os.path.join(static_path, "js", "test.js")
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response, "Response should be None")

    def test_redirection_disable(self):
        '''
        Accessing somewhere not listed on the disable list,
        the middleware should redirect
        '''
        from django.conf import settings
        setattr(
            settings,
            "DISABLE_REDIRECT",
            [
                r"^disable_redirection",
                r"^also_disable_redirection"
            ]
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "The response should be HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#" + self.path,
            "The path should be prefixed with /#"
        )

    def test_disable_redirection(self):
        '''
        Accessing somewhere listed on the disable list,
        the middleware shouldn't redirect
        '''
        from django.conf import settings
        setattr(
            settings,
            "DISABLE_REDIRECT",
            [
                r"^disable_redirection",
                r"^also_disable_redirection"
            ]
        )
        self.request = HTTPRequest(
            False,
            "/also_disable_redirection/test?num=5585"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response)

    def test_disable_redirection_cp(self):
        '''
        Accessing somewhere listed on the disable list,
        the middleware shouldn't redirect (Complex ver.)
        '''
        from django.conf import settings
        setattr(
            settings,
            "DISABLE_REDIRECT",
            [
                r"^disable_redirection/test[1-9]{3}/article[s]{0,1}/[0-9]{5}",
                r"^disable_redirection/test[1-9]{5,8}/.$"
            ]
        )
        self.request = HTTPRequest(
            False,
            "/disable_redirection/test?num=5585"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "The response should be HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#/disable_redirection/test?num=5585",
            "The path should be prefixed with /#"
        )
        self.request = HTTPRequest(
            False,
            "/disable_redirection/test567/articles/05895"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response)
        self.request = HTTPRequest(
            False,
            "/disable_redirection/test567/articles/05895/images/test.jpg"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response)
        self.request = HTTPRequest(
            False,
            "/disable_redirection/test5675/articles/05895/images/test.jpg"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "The response should be HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#/disable_redirection/test5675/articles/05895/images/test.jpg",
            "The path should be prefixed with /#"
        )

        self.request = HTTPRequest(
            False,
            "/disable_redirection/test56675/articles/05895/images/test.jpg"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsInstance(
            response,
            HttpResponseRedirect,
            "The response should be HttpResponseRedirect"
        )
        self.assertEqual(
            response.url,
            "/#/disable_redirection/test56675/articles/05895/images/test.jpg",
            "The path should be prefixed with /#"
        )

        self.request = HTTPRequest(
            False,
            "/disable_redirection/test56675/b"
        )
        response = AjaxRedirectionMiddleware().process_request(self.request)
        self.assertIsNone(response)
