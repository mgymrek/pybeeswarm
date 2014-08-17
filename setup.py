from setuptools import setup

DESCRIPTION = "Beeswarm plots for python"
LONG_DESCRIPTION = DESCRIPTION
NAME = "pybeeswarm"
AUTHOR = "Melissa Gymrek"
AUTHOR_EMAIL = "mgymrek@mit.edu"
MAINTAINER = "Melissa Gymrek"
MAINTAINER_EMAIL = "mgymrek@mit.edu"
DOWNLOAD_URL = 'https://github.com/mgymrek/pybeeswarm'
LICENSE = 'MIT'

VERSION = '1.0.0'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      url=DOWNLOAD_URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=['beeswarm'],
      package_dir={'beeswarm': 'beeswarm'},
      install_requires=['matplotlib','numpy','pandas'],
      classifiers=['Development Status :: 4 - Beta',\
                       'Programming Language :: Python :: 2.7',\
                       'License :: OSI Approved :: MIT License',\
                       'Operating System :: OS Independent',\
                       'Intended Audience :: Science/Research',\
                       'Topic :: Scientific/Engineering :: Visualization']
     )
