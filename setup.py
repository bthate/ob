# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='ob',
    version='103',
    description="python3 object library",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate/ob',
    long_description=read(),
    license='Public Domain',
    package_dir={'': 'lib'},
    py_modules=['ob','hdl', 'prs', 'run', 'thr'],
    include_package_data=True,
    data_files=[('om', ['om/adm.py',
                        'om/cms.py',
                        'om/fnd.py',
                        'om/irc.py',
                        'om/log.py',
                        'om/rss.py',
                        'om/tdo.py',
                        'om/udp.py'])],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
