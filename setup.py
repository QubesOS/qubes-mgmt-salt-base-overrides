# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name               = 'qubes.mgmt.patches',
      version            = '1.0',
      author             = 'Jason Mehring',
      author_email       = 'nrgaway@gmail.com',
      url                = 'https://github.com/nrgaway/qubes-mgmt-salt-base-overrides',
      packages           = ['qubes', 'qubes.mgmt', 'qubes.mgmt.patches'],
      package_dir        = {'': 'src'},
      license            ='LICENSE',
      description        = 'Custom modules to override existing Salt modules ' \
		           'due to upstream bugs or implementation conflicts.',
      long_description   = open('README.rst').read()
      )
