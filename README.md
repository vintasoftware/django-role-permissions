# django-role-permissions

[![Build Status](https://github.com/vintasoftware/django-role-permissions/actions/workflows/build.yml/badge.svg)](https://github.com/vintasoftware/django-role-permissions/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/vintasoftware/django-role-permissions/badge.svg?branch=master)](https://coveralls.io/github/vintasoftware/django-role-permissions?branch=master)
[![Current version at PyPI](https://img.shields.io/pypi/v/django-role-permissions.svg)](https://pypi.python.org/pypi/django-role-permissions)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/django-role-permissions.svg)

``django-role-permissions`` is a django app for role based permissions. It's built on top of django ``contrib.auth`` user ```Group``` and ``Permission`` functionalities and it does not add any other models to your project.  

``django-role-permissions`` supports Django versions from 1.5 until the latest.

Version 2.x now supports multiple roles!

## Documentation

Documentation is available at:

[http://django-role-permissions.readthedocs.org/](http://django-role-permissions.readthedocs.org/)

If you are still using the 1.x version the old documentation is at:

[http://django-role-permissions.readthedocs.io/en/1.x/](http://django-role-permissions.readthedocs.io/en/1.x/)

## Running tests

This packages uses `tox` to run tests on multiple evironments, please make sure they are passing before submitting a pull request.
To run tests, install tox and run it in the command line from this project's folder:

``$ tox``

## Maintainers

### How to Release:

#### Pre release:
- Include the changes in `CHANGELOG`
- Update the version in `rolepermissions/__init__.py`
- Update the classifiers in `setup.py`

#### Release:
- Run the github action [release](https://github.com/vintasoftware/django-role-permissions/actions/workflows/release.yml)

#### Post release:
- Check if docs were updated at [readthedocs](http://django-role-permissions.readthedocs.org/).

## Help

If you have any questions or need help, please send an email to: contact@vinta.com.br

## Commercial Support

[![alt text](https://avatars2.githubusercontent.com/u/5529080?s=80&v=4 "Vinta Logo")](https://www.vinta.com.br/)

This project is maintained by [Vinta Software](https://www.vinta.com.br/) and is used in products of Vinta's clients. We are always looking for exciting work, so if you need any commercial support, feel free to get in touch: contact@vinta.com.br

Copyright (c) 2019 Vinta Serviços e Soluções Tecnológicas Ltda.
[MIT License](LICENSE.txt)
