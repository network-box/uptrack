from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated

from .models import DBSession, Release


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


class BaseResource(object):
    __name__ = None
    __parent__ = None

    def __getitem__(self, id):
        o = DBSession.query(self.__model__).get(id)
        if o:
            o.__parent__ = self
            o.__name__ = id
            return o

        else:
            raise KeyError(id)


class ReleaseResource(BaseResource):
    __model__ = Release


def get_root(request):
    global resources
    resources.update({"releases": ReleaseResource,
                      })

    return RootFactory(request)
