from django.contrib import admin
from hvad.admin import TranslatableAdmin
from cockpit.models import Page


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

admin.site.register(Page, PageAdmin)