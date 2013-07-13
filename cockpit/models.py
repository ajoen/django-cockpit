from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
from noconflict import classmaker
import mptt


class Page(TranslatableModel):
    """
    Pages with hierarchical structure.
    """

    # Prevent metaclass conflict
    # https://github.com/ojii/django-nani/issues/39
    # http://code.activestate.com/recipes/204197-solving-the-metaclass-conflict/
    #__metaclass__=classmaker()

    translations = TranslatedFields(
        heading=models.CharField(_('heading'), max_length=200, unique=True),
        content=RichTextField(_('content')),
        slug=models.SlugField(_('slug'), unique=True,)
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.heading

TreeForeignKey(Page, blank=True, null=True).contribute_to_class(Page, 'parent')

mptt.register(Page)