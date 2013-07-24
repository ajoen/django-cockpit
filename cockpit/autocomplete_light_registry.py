import autocomplete_light
from cockpit.models import Page
from autocomplete_light.contrib.hvad import AutocompleteModelBase

autocomplete_light.registry.autocomplete_model_base = AutocompleteModelBase

autocomplete_light.register(Page, AutocompleteModelBase,
    search_fields=['heading'],
    autocomplete_js_attributes={'placeholder': 'Parent name...'},
)