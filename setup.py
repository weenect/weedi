from setuptools import setup, find_packages

VERSION = '0.1'

setup(
  name = 'weedi',
  packages = find_packages(),
  version = VERSION,
  description = 'A dependency injection system using setuptools entry points',
  author = 'Weenect',
  url = 'https://github.com/weenect/weedi',
  download_url = 'https://github.com/weenect/weedi/' + VERSION,
  keywords = ['di', 'dependency injection', 'entry points', 'services', 'setuptools'],
  classifiers = [],
  install_requires=('configobj'),
  test_suite = "weedi.tests"
)
