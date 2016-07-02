Package source code
===================
python setup.py sdist

Package universal binary
========================
python setup.py bdist_wheel --universal

Upload
======
twine upload dist/<*|filename(s)>