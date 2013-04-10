# There is a conflict with older versions on EL 6
__requires__ = ['PasteDeploy>=1.5.0',
                'WebOb>=1.2b3',
                ]

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='uptrack',
      version='0.0',
      description='uptrack',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='uptrack',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = uptrack:main
      [console_scripts]
      initialize_uptrack_db = uptrack.scripts.initializedb:main
      """,
      )
