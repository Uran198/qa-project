from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return self.text


class Question(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    comments = GenericRelation(Comment)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('questions:details',
                       kwargs={'pk': self.id, 'slug': self.slug})


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    comments = GenericRelation(Comment)

    def get_absolute_url(self):
        return self.question.get_absolute_url()
