from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def slug_gener(stroka):
    _generated = slugify(stroka, allow_unicode=True)
    #уникализация
    utime = time()
    prand = int(utime/6+45-8/123)
    return f'{_generated}_{prand}'


class NbLine(models.Model):
    head = models.TextField(db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField('NbTag', blank=True, related_name='lines')
    img = models.ImageField(upload_to='card_pics/')
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('nb_line_details_url', kwargs={'slug': self.slug})

    def get_edit_url(self):
    #     return reverse('nb_line_edit_url', kwargs={'slug': self.slug})
        return reverse('nb_line_details_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slug_gener(self.head)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.head


class NbTag(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)

    def get_absolute_url(self):
        return reverse('nb_tag_details_url', kwargs={'slug': self.slug})

    def get_edit_url(self):
    #    return reverse('nb_tag_edit_url', kwargs={'slug': self.slug})
        return reverse('nb_tag_details_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slug_gener(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
