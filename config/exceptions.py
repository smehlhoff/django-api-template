from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound('Page not found.')

    response = exception_handler(exc, context)
    handlers = {
        'MethodNotAllowed': method_not_allowed,
        'UnsupportedMediaType': unsupported_media,
        'ValidationError': validation_error,
    }
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    response.data = {
        'error': {
            'message': exc.detail
        }
    }

    return response


def method_not_allowed(exc, context, response):
    response.data = {
        'error': {
            'message': 'Method not allowed.'
        }
    }

    return response


def unsupported_media(exc, context, response):
    response.data = {
        'error': {
            'message': 'Unsupported media type.'
        }
    }

    return response


def validation_error(exc, context, response):
    response.data = {
        'errors': response.data
    }

    return response
