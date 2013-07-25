import autocomplete_light
from cockpit.models import Page

autocomplete_light.register(Page,
    search_fields=['translations__heading'],
    autocomplete_js_attributes={'placeholder': 'Parent name...'},
)