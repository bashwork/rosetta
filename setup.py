#!/usr/bin/env python
'''
Installs rosetta using distutils

Run:
    python setup.py install
to install the package from the source archive.

For information about setuptools
http://peak.telecommunity.com/DevCenter/setuptools
'''

from setuptools import setup, find_packages
from distutils.core import Command
import sys, os

#---------------------------------------------------------------------------# 
# Extra Commands
#---------------------------------------------------------------------------# 
command_classes = {}

class BuildApiDocs(Command):
    ''' Helper command to build the available api documents
    This scans all the subdirectories under api and runs the
    build.py script underneath trying to build the api
    documentation for the given format.
    '''
    user_options = []

    def initialize_options(self):
        ''' options setup '''
        pass

    def finalize_options(self):
        ''' options teardown '''
        pass

    def run(self):
        ''' command runner '''
        old_cwd = os.getcwd()
        for entry in os.listdir('./api'):
            os.chdir('./api/%s' % entry)
            os.system('python build.py')
            os.chdir(old_cwd)

command_classes['build_apidocs'] = BuildApiDocs

#---------------------------------------------------------------------------# 
# Configuration
#---------------------------------------------------------------------------# 
from pymodbus import __version__

setup(name  = 'rosetta',
    version = __version__,
    description = "A write once protocol builder",
    long_description='''
    Pymodbus aims to be a fully implemented modbus protocol stack implemented
    using twisted.  Its orignal goal was to allow simulation of thousands of
    modbus devices on a single machine for monitoring software testing.
    ''',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
        'Topic :: Utilities'
    ],
    keywords = 'protocol, network, testing',
    author = 'Galen Collins',
    author_email = 'bashwork@gmail.com',
    maintainer = 'Galen Collins',
    maintainer_email = 'bashwork@gmail.com',
    url='http://code.google.com/p/rosetta/',
    license = 'LGPL',
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests', 'doc']),
    platforms = ["Linux","Mac OS X","Win"],
    include_package_data = True,
    zip_safe = True,
    install_requires = [
        'nose >= 0.9.3'
    ],
    test_suite = 'nose.collector',
    cmdclass = command_classes,
)
