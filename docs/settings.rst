==========================
Settings
==========================


Redirect to the login page
==========================

Instead of getting a Forbidden (403) error when the user has no permission, you can make the request be redirected to the login page.
Add the following variable to your django ``settings.py``:

``settings.py``

.. code-block:: python

    ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True
