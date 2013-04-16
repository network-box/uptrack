# There is a conflict with older versions on EL 6
__requires__ = ['PasteDeploy>=1.5.0',
                'WebOb>=1.2b3',
                ]

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'py-bcrypt',
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
      author='Mathieu Bridon',
      author_email='mathieu.bridon@network-box.com',
      url='',
      license='AGPLv3+',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='uptrack',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = uptrack:main
      [console_scripts]
      uptrack-initdb = uptrack.scripts.initializedb:main
      """,
      )
