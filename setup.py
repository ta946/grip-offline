"""
Grip
----

Render local markdown files offline.


Grip is easy to set up
``````````````````````

::

    $ cd grip-offline
    $ pip install .
    $ cd myproject
    $ grip


Links
`````

* `Website <https://github.com/ta946/grip-offline>`_

"""

import os
from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='grip-offline',
    version='4.6.2',
    description='Render local markdown files offline.',
    long_description=__doc__,
    author='ta946',
    url='https://github.com/ta946/grip-offline',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={'grip': ['static/*.*', 'static/octicons/*', 'templates/*']},
    install_requires=read('requirements.txt').splitlines(),
    extras_require={'tests': read('requirements-test.txt').splitlines()},
    zip_safe=False,
    entry_points={'console_scripts': ['grip = grip:main']},
)
