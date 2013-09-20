#!/usr/bin/env python

from setuptools import setup

setup(name		    = 'zonepull',
      version		= '0.1',
      description	= 'attempt a full zone dump on each nameserver for a given domain',
      author		= 'kaizoku',
      author_email	= 'kaizoku@phear.cc',
      py_modules	= ['zonepull'],
      license		= 'WTF',
      url		    = 'http://github.com/kaizoku/zonepull',
      entry_points  = {
          'console_scripts': ['zonepull = zonepull.zonepull:main']
          },
      install_requires  = ['dnspython'],
)
