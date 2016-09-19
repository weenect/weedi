Update VERSION in setup.py
commit
tag

virtualenv -p python3.4 venv
. venv/bin/activate
pip install setuptools --upgrade
pip install wheel
pip install twine

python setup.py sdist
twine upload dist/weedi-VERSION.tar.gz

python3 setup.py bdist_wheel --universal
twine upload dist/weedi-VERSION-py2.py3-none-any.whl
