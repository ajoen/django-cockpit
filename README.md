django-cockpit
==============

Dead simple CMS for django 1.5+

Quick start
-----------

1. Add "cockpit" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'cockpit',
      )

2. Include the cockpit URLconf in your project urls.py like this::

      url(r'^cockpit/', include('cockpit.urls')),

3. Run `python manage.py syncdb` to create the cockpit models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create pages (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/cockpit/ to participate in the pages.

## License

django-cockpit is licensed under the terms of the Apache License, version 2.0. For more information, see LICENSE file.
