# -*- coding: utf-8 -*-

import pkgutil


# import all submodules in this folder, to run all decorators
__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__,
                                                      prefix=__name__ + '.'):
    __import__(modname)
