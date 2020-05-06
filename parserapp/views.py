from django.shortcuts import render
from .utils import *
from .models import PaVacancies, PaResumes, PaSettingsVacancies, PaSettingsResumes
from django.views.generic import View
from .mixins import MixinResults, MixinRefreshdb



class PaShowResultsVacancies(MixinResults, View):
    key_word = 'vacancy' # vacancy or resume
    raise_exception = True


class PaShowResultsResumes(MixinResults, View):
    key_word = 'resume' # vacancy or resume
    raise_exception = True


class PaRefreshdbVacancies(MixinRefreshdb, View):
    key_word = 'vacancy' # vacancy or resume
    raise_exception = True


class PaRefreshdbResumes(MixinRefreshdb, View):
    key_word = 'resume' # vacancy or resume
    raise_exception = True
