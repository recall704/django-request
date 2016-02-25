# -*- coding: utf-8 -*-
from .models import Request
import settings as request_settings
from .router import patterns


class RequestMiddleware(object):
    def process_response(self, request, response):
        if request.method.lower() not in request_settings.REQUEST_VALID_METHOD_NAMES:
            return response

        if response.status_code < 400 and request_settings.REQUEST_ONLY_ERRORS:
            return response

        ignore = patterns(False, *request_settings.REQUEST_IGNORE_PATHS)
        if ignore.resolve(request.path[1:]):
            return response

        if request.is_ajax() and request_settings.REQUEST_IGNORE_AJAX:
            return response

        if request.META.get('REMOTE_ADDR') in request_settings.REQUEST_IGNORE_IP:
            return response

        ignore = patterns(False, *request_settings.REQUEST_IGNORE_USER_AGENTS)
        if ignore.resolve(request.META.get('HTTP_USER_AGENT', '')):
            return response

        if getattr(request, 'user', False):
            if request.user.username in request_settings.REQUEST_IGNORE_USERNAME:
                return response

        r = Request()
        r.from_http_request(request, response)

        return response
