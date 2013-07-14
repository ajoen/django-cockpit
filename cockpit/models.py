from django.db import models
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField


class Page(TranslatableModel):
    """
    Pages with hierarchical structure.
    """

    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True)

    translations = TranslatedFields(
        heading=models.CharField(_('heading'), max_length=200, unique=True),
        content=RichTextField(_('content')),
        slug=models.SlugField(_('slug'), unique=True)
    )

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return u"%s" % self.lazy_translation_getter('heading')