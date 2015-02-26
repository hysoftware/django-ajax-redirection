#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
Request Mocks
'''


class HTTPRequest(object):
    '''
    The mock of HTTPRequest.
    '''
    url = None
    ajax = False

    def __init__(self, ajax, path):
        '''
        Constructor
        '''
        self.ajax = ajax
        self.url = path

    def is_ajax(self):
        '''
        Returns is_ajax
        '''
        return self.ajax

    def get_full_path(self):
        '''
        Returns the path.
        '''
        return self.url
