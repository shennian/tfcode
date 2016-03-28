def outer(x):
    def inner():
        print x
    return inner


a = outer(1)
a()
#

'''
decorator- the core is function
'''


def route(path, **kwargs):#path and metho
    name = None
    if path.count('<') == 1 and path.count('>') == 1\
            and path.index('<') < path.index('>'):
        name = path[path.index('<'): path.index('>')]

    def fuck(function):
        if name is None:
            def inner():
                return function()
        else:
            def inner(name):
                return function(name)
        return inner
    return fuck


@route("/main/<name>", methods=['post', 'get'])
def index(name):
    print name
    return "hello world"

index(233)
