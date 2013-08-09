from django.conf import settings

ADMIN_PAGE_SELECTION = getattr(settings, 'COCKPIT_ADMIN_PAGE_SELECTION', 'selectbox')