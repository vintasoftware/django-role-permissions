=====
Setup
=====

Installation
============

Install from PyPI with ``pip``::

    pip install django-role-permissions


Configuration
=============

Add ```rolepermissions``` to you ```INSTALLED_APPS```

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rolepermissions',
        ...
    )


Add the register to your ```urls.py```

.. code-block:: python

    from rolepermissions.loader import load_roles_and_permissions
    load_roles_and_permissions()
