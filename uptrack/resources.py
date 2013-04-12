from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated


resources = {}


class RootFactory(object):
    __name__ = 'RootFactory'
    __parent__ = None
    __acl__ = [(Allow, Authenticated, ALL_PERMISSIONS)]

    def __init__(self, request):
        pass

    def __getitem__(self, name):
        r = resources[name]()
        r.__parent__ = self
        r.__name__ = name
        return r


def get_root(request):
    return RootFactory(request)
