# There is a conflict with older versions on EL 6
__requires__ = ['PasteDeploy>=1.5.0',
                'WebOb>=1.2b3',
                ]

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'zope.sqlalchemy',
    'waitress',
    'py-bcrypt',

    # Bump the needed version once this bug is fixed:
    # https://github.com/Kotti/deform_bootstrap/pull/54
    'deform_bootstrap',

    # These are not available from Pypi
    # 'koji',
    # 'rpm',
    # 'yum',
    ]

setup(name='uptrack',
      version='0.0',
      description='Upstream distribution version tracking',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Mathieu Bridon',
      author_email='mathieu.bridon@network-box.com',
      url='https://gitorious.org/bochecha-dayjob/uptrack',
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
      uptrack-sync = uptrack.scripts.sync:main
      """,
      )
