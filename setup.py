from setuptools import setup, find_packages

VERSION = '0.1'


setup(
  name='weedi',
  packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
  version=VERSION,
  description='A dependency injection system using setuptools entry points',
  author='Weenect',
  url='https://github.com/weenect/weedi',
  download_url='https://github.com/weenect/weedi/tarball/' + VERSION,
  keywords=['di', 'dependency injection', 'entry points', 'entry_points', 'setuptools'],
  install_requires=('configobj'),
  tests_require=('mock'),
  extras_require={'test': ('mock')},
  setup_requires=['setuptools-pep8'],
  test_suite="weedi.tests"
)
