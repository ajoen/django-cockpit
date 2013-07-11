from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


class Page(MPTTModel):
    header = models.CharField(max_length=200, unique=True)
    content = RichTextField()
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    created_at = models.DateTimeField('created at', auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['header']

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.header
