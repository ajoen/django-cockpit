from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

class Page(models.Model):
    header = models.CharField(max_length=200)
    content = RichTextField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.header
