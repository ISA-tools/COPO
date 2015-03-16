__author__ = 'felixshaw'

class Resource(object):
    def GET(self, request, **kwargs):
        return NotImplemented()

    def HEAD(self, request, **kwargs):
        return NotImplemented()

    def POST(self, request, **kwargs):
        return NotImplemented()

    def DELETE(self, request, **kwargs):
        return NotImplemented()

    def PUT(self, request, **kwargs):
        return NotImplemented()

    def __call__(self, request, **kwargs):
        handler = getattr(self, request.method)
        return handler(request, **kwargs)