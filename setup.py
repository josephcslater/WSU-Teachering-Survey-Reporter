#!/usr/bin/env python

from setuptools import setup
import os
import sys

if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported.')
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

'''download_url = ('https://github.com/Vibration-Testing/vibrationtesting/\
                blob/master/dist/vibrationtesting-' + version + '.whl')'''

setup(name='WSU_Teaching_Survey_Reporter',
      version=1.0,
      description=('WSU_Teaching_Survey_Reporter'),
      author=u'Joseph C. Slater',
      author_email='joseph.c.slater@gmail.com',
      url='https://github.com/josephcslater/WSU_Teaching_Survey_Reporter',
      packages=['WSU_Teaching_Survey_Reporter'],
      package_data={'': ['readme.rst']},
      long_description=read('readme.rst'),
      keywords=['Wright State University', 'Teaching Evaluations'],
      install_requires=['numpy', 'pandas', 'pivottablejs'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
      )

# https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
