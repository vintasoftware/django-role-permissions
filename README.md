# django-role-permissions

[![Build Status](https://travis-ci.org/vintasoftware/django-role-permissions.svg?branch=master)](https://travis-ci.org/vintasoftware/django-role-permissions)
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

## Version 1.x support

No new features will be added to version 1.x, neither is it going to be officially supported. However, there's still a [1.x](https://github.com/vintasoftware/django-role-permissions/tree/1.x) branch. PRs and bug fixes are welcome there and we may push new versions to PyPI.

## 2.x release notes

There are major changes from version 1.x to 2.x. Here are some of them worth noting:

- Django role permissions now supports multiple role attribution
- Function names have changed to adapt to multiple roles
- Import paths have changed

A special thanks to [@kavdev](https://github.com/kavdev) for working on multiple role support.

## Running tests

This packages uses `tox` to run tests on multiple evironments, please make sure they are passing before submitting a pull request.
To run tests, install tox and run it in the command line from this project's folder:

``$ tox``

## Help

If you have any questions or need help, please send an email to: contact@vinta.com.br

## Commercial Support
[![alt text](https://avatars2.githubusercontent.com/u/5529080?s=200&v=4 "Vinta Logo")](https://vintasoftware.com)

This project, as other Vinta open-source projects, is used in products of Vinta's clients. We are always looking for exciting work, so if you need any commercial support, feel free to get in touch: contact@vinta.com.br

Copyright (c) 2019 Vinta Serviços e Soluções Tecnológicas Ltda.
[MIT License](LICENSE.txt)
