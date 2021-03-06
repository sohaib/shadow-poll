#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import sys, os
from os import path

# figure out where all the extra libs (rapidsms and contribs) are
libs=[os.path.abspath('lib'),os.path.abspath('apps')] # main 'rapidsms/lib'
try:
    for f in os.listdir('contrib'):
        pkg = path.join('contrib',f)
        if path.isdir(pkg) and 'lib' in os.listdir(pkg):
            libs.append(path.abspath(path.join(pkg,'lib')))
except:
                # could be several reasons:
                        # no 'contrib' dir, 'contrib' not a dir
                        # 'contrib' not readable, in any case
                        # ignore and leave 'libs' as just
                        # 'rapidsms/lib'
    pass

# add extra libs to the python sys path
sys.path.extend(libs)

# import manager now that the path is correct
from rapidsms import manager

if __name__ == "__main__":
    manager.start(sys.argv)
