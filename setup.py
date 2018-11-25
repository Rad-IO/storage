from setuptools import setup

DESCRIPTION = 'Storage utilities for the Rad-I/O project.'
LONG_DESCR = DESCRIPTION

setup(
    name='radio_storage',
    version='0.0.1',
    description=DESCRIPTION,
    long_description=LONG_DESCR,
    url='https://gitlab.com/',
    author='Rad-I/O',
    author_email='a96tudor@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ],
    keywords='Rad-I/O storage',
    packages=['storage', 'storage.drivers', 'storage.handler_user',
              'storage.handler_ml'],
    install_requires=[
        'numpy', 'psycopg2', 'tensorflow', 'passlib',
    ],
)
