from django.contrib import admin
from .models import PaVacancies, PaResumes, PaSettingsVacancies, PaSettingsResumes


admin.site.register(PaVacancies)
admin.site.register(PaResumes)
admin.site.register(PaSettingsVacancies)
admin.site.register(PaSettingsResumes)
