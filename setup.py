# This file is place in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='ob',
    version='111',
    description="python3 object library",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate/ob',
    long_description=read(),
    license='Public Domain',
    py_modules=["ob", "om", "on"],
    scripts=["bin/ob"],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
