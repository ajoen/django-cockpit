from django.contrib import admin
from hvad.admin import TranslatableAdmin
from cockpit.models import Page
from cockpit.widgets import CockpitPageSelectWidget, CKEditorWidgetCockpit
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect
import autocomplete_light
from cockpit.settings import ADMIN_PAGE_SELECTION


class PageAdmin(TranslatableAdmin):
    class Meta:
        model = Page

    #
    # Workaround for prepopulated_fields and fieldsets from here:
    # https://github.com/KristianOellegaard/django-hvad/issues/10#issuecomment-5572524
    #
    def __init__(self, *args, **kwargs):
        super(PageAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ('heading',)}

    list_display = ('__str__', 'all_translations', 'created_at', 'parent')
    list_filter = ['created_at']
    search_fields = ['translations__heading']
    date_hierarchy = 'created_at'

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Specified widgets for the fields.
        """
        if db_field.name == 'content':
            kwargs['widget'] = CKEditorWidgetCockpit
        if db_field.name == 'parent':
            if ADMIN_PAGE_SELECTION == 'selectbox':
                kwargs['widget'] = CockpitPageSelectWidget
            else:
                kwargs['widget'] = autocomplete_light.ChoiceWidget('PageAutocompleteModelBase')
        return super(PageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_urls(self):
        """
        Overrided to include a custom admin page "change_parent".
        """
        urls = super(PageAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^change_parent/$', self.admin_site.admin_view(self.change_parent), name='change_parent')
        )
        return my_urls + urls

    def change_parent(self, request):
        """
        This view receives "next", "change_parent_of" and "change_parent_to" parameters
        and changes page hierarchy accordingly. Redirects to the "next" parameter
        afterwards.
        """
        redirect_to = request.GET['next']
        change_parent_of = Page.objects.get(pk=request.GET['change_parent_of'])
        change_parent_to = Page.objects.get(pk=request.GET['change_parent_to'])
        change_parent_of.parent_id = change_parent_to.id

        # Check if there is cycle in the tree.
        parent_cycle = change_parent_to
        while True:
            if parent_cycle.parent_id is None:
                break
            if parent_cycle.parent_id == change_parent_of.id:
                parent_cycle.parent_id = None
                break
            parent_cycle = Page.objects.get(pk=parent_cycle.parent_id)

        change_parent_of.save()
        parent_cycle.save()
        return HttpResponseRedirect(redirect_to)

admin.site.register(Page, PageAdmin)