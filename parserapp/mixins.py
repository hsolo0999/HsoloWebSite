from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import os
import random
from pprint import pprint
from .forms import *
from .views import *



class MixinResults:

    key_word = None # vacancy or resume

    def get(self, request):
        print(f'====MIXINRESULTS_GET [START]')
        # load settings from DB

        if self.key_word == 'vacancy':
            print(f'====MIXINRESULTS_GET mode {self.key_word}')
            setts = PaSettingsVacancies.objects.last()
            form = SettingsFormVacancies(instance=setts)
            template = 'parserapp/parse_res.html'
        elif self.key_word == 'resume':
            print(f'====MIXINRESULTS_GET mode {self.key_word}')
            setts = PaSettingsResumes.objects.last()
            form = SettingsFormResumes(instance=setts) 
            template = 'parserapp/parse_res_resumes.html'

        vacancies, resumes = parse_vacsrezumes(setts)

        context = read_db(request, setts, self.key_word)
        context['form'] = form
        context['pasettings'] = setts
        context['vacancies'] = vacancies
        context['resumes'] = resumes

        pprint(f'====MIXINRESULTS_GET [STOP]')

        return render(request, template, context=context)

    def post(self, request):
        print(f'====MIXINRESULTS_GET [START]')

        if self.key_word == 'vacancy':
            obj = PaSettingsVacancies.objects.last()
            form = SettingsFormVacancies(request.POST, instance=obj)
            re_link = 'pr_result_vacancies_url'
            template = 'parserapp/parse_res.html'
        elif self.key_word == 'resume':
            obj = PaSettingsResumes.objects.last()
            form = SettingsFormResumes(request.POST, instance=obj)
            re_link = 'pr_result_resumes_url'
            template = 'parserapp/parse_res_resumes.html'

        if form.is_valid():
            edited_obj = form.save(commit=True)
            print(f'====MIXINRESULTS_GET [STOP]')
            return redirect(re_link)
        print(f'====MIXINRESULTS_GET [STOP]')
        return render(request,
                        template,
                        context={'form': form, 'pasettings': edited_obj})


class MixinRefreshdb:

    key_word = None # vacancy or resume

    def get(self, request):
        pprint(f'===MIXINREFRESHDB [START]')

        if self.key_word == 'vacancy':
            pprint(f'===MIXINREFRESHDB mode {self.key_word}')
            setts = PaSettingsVacancies.objects.last()
            re_link = 'pr_result_vacancies_url'
        elif self.key_word == 'resume':
            pprint(f'===MIXINREFRESHDB mode {self.key_word}')
            setts = PaSettingsResumes.objects.last()
            re_link = 'pr_result_resumes_url'

        clean_db(self.key_word)

        if self.key_word == 'vacancy':
            res_tup = parse_html_vacancies(setts)
        elif self.key_word == 'resume':
            res_tup = parse_html_resumes(setts)

        save_db(res_tup, self.key_word)

        pprint(f'===MIXINREFRESHDB [STOP]')

        return redirect(re_link)
