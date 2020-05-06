from django.db import models


class PaVacancies(models.Model):
    number = models.IntegerField(db_index=True, default=0)
    title = models.TextField(blank=True)
    url = models.TextField(blank=True)
    company = models.TextField(blank=True)
    compensation = models.TextField(blank=True)
    date_publicate = models.TextField(blank=True)
    status = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.title


class PaResumes(models.Model):
    number = models.IntegerField(db_index=True, default=0)
    title = models.TextField(blank=True)
    url = models.TextField(blank=True)
    exp = models.TextField(blank=True)
    educate = models.TextField(blank=True)
    refresh = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.title


class PaSettingsVacancies(models.Model):
    url_base = models.TextField(default='https://hh.ru/search/vacancy')
    query = models.CharField(max_length=50, default='python')
    region = models.IntegerField(default=1)
    page = models.IntegerField(default=0)
    show_items = models.IntegerField(default=10)
    threads = models.IntegerField(default=5)

    def __str__(self):
        return self.query


class PaSettingsResumes(models.Model):
    url_base = models.TextField(default='https://hh.ru/search/resume?clusters=true&exp_period=all_time&logic=normal&pos=full_text&st=resumeSearch')
    query = models.CharField(max_length=50, default='python')
    region = models.IntegerField(default=1)
    page = models.IntegerField(default=0)
    show_items = models.IntegerField(default=10)
    threads = models.IntegerField(default=5)

    def __str__(self):
        return self.query
