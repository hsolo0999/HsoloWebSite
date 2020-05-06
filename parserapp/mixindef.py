# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from builtins import super
from .constants import Const
from django.core.paginator import Paginator
import logging
from .models import PaVacancies, PaResumes
from pprint import pprint
import requests
from random import choice
import sys
from threading import Thread
from time import time, sleep


logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', filename="parserapp/LOG.log", level=logging.DEBUG, filemode='w')


#переопределение класса треда для получения результата функции таргета
#--------------------------------------------------
#get Python version
if sys.version_info >= (3, 0):
    # code for Python 3
    _thread_target_key = '_target'
    _thread_args_key = '_args'
    _thread_kwargs_key = '_kwargs'
else:
    #code for Python 2
    _thread_target_key = '_Thread__target'
    _thread_args_key = '_Thread__args'
    _thread_kwargs_key = '_Thread__kwargs'

#initialization of the new class for Thread
class ThreadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        target = getattr(self, _thread_target_key)
        if not target is None:
            self._return = target(*getattr(self, _thread_args_key), **getattr(self, _thread_kwargs_key))

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return
#---------------------------------------------------------


class MixinGetHtml:
    """
    Formation URL -> formation REQUEST -> get RESPONSE as HTML document ->
    -> return HTML document
    """

    base_url = None
    params = None

    def get_html(self):
        base_url = self.base_url
        headers = {'user-agent': choice(Const.useragents)}
        proxies = {'http': choice(Const.proxys)}
        params = self.params

        request_get = requests.get(base_url,
                                    headers=headers,
                                    proxies=proxies,
                                    params=params)

        if request_get.ok == True: #_req.statuscode == 200...300
            html = request_get.content
        else:
            logging.info(f'MixinGetHtml return status_code = {request_get.status_code}')
            html = None
        return html


class MixinGlobalParseHtml:
    """
    Receives HTML from func get_html -> parse each HTML ->
    -> return objects params in dictionary
    """

    show_items = None
    threads = None
    base_url = None
    params = None
    key_word = None #resume or vacancy

    def parse_html(self):
        counter = 0
        titles_list = []
        companies_list = []
        compensations_list = []
        publicates_list = []
        bads_or_goods_list = []
        exp_list = []
        educations_list = []
        refreshs_list = []
        urls_list = []
        objects_dict = dict()
        threads_list_publicate = []
        threads_list_badorgood = []
        threads_list_education = []

        ge = MixinGetHtml()
        ge.base_url = self.base_url
        ge.params = self.params
        html = ge.get_html()
        main_block = bs(html, 'lxml')
        objects = main_block.find_all('div', attrs={'data-qa': f'{self.key_word}-serp__{self.key_word}'})
        for obj in objects:
##################################VACANCY#############################################
            if self.key_word == 'vacancy':
                try: #title
                    title = obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                except Exception as Ex:
                    logging.info(f'====exept in vacancy "title" {Ex.args}')
                    title = 'Error (see on the log)'
                try: # urls
                    urls = obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                except Exception as Ex:
                    logging.info(f'====exept in vacancy "urls" {Ex.args}')
                    urls = 'Error (see on the log)'
                try: # company
                    company = obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                except Exception as Ex:
                    logging.info(f'====exept in vacancy "company" {Ex.args}')
                    company = 'Error (see on the log)'
                try: # compensation
                    compensation = obj.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                except Exception as Ex:
                    logging.info(f'====exept in vacancy "compensation" {Ex.args}')
                    compensation = '-'

                    titles_list.append(title)
                    urls_list.append(urls)
                    companies_list.append(company)
                    compensations_list.append(compensation)
#######################################################################################
######################################RESUME###########################################
            elif self.key_word == 'resume':
                try: # title
                    title = obj.find('a', attrs={'data-qa': 'resume-serp__resume-title'}).text
                except Exception as Ex:
                    logging.info(f'====exept in resume "title" {Ex.args}')
                    title = 'Error (see on the log)'
                try: # urls
                    url = obj.find('a', attrs={'data-qa': 'resume-serp__resume-title'})['href']
                    urls = f'https://hh.ru{url}'
                except Exception as Ex:
                    logging.info('====exept in resume "urls" {Ex.args}')
                    urls = f'https://hh.ru/404'
                try: # company
                    company = obj.find('span', attrs={'class': 'bloko-link-switch bloko-link-switch_inherited'}).text
                except Exception as Ex:
                    logging.info(f'====exept in "company" {Ex.args}')
                    company = 'Error (see on the log)'
                try: # refresh
                    refresh = obj.find('span', attrs={'class': 'resume-search-item__date'}).text
                except Exception as Ex:
                    logging.info(f'====exept in "refresh" {Ex.args}')
                    refresh = '-'

                titles_list.append(title)
                urls_list.append(urls)
                exp_list.append(company)
                refreshs_list.append(refresh)
######################################################################################

#####################################VACANCY##########################################
        if self.key_word == 'vacancy':
            from parserapp.utils import parse_vacancy_publicate, parse_bad_vacancy
            start = time()
            #creating a threads lists for 2 funcs
            counter = 0

            for url in urls_list:
                if counter <= self.threads:
                    url_strip = url.strip()
                    thread = ThreadWithReturn(target=parse_vacancy_publicate, args=( url_strip, ))
                    threads_list_publicate.append(thread)
                    thread = ThreadWithReturn(target=parse_bad_vacancy, args=( url_strip, ))
                    threads_list_badorgood.append(thread)
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (vacancy) открыл {counter}-й тред')
                    counter += 1
                else:
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (vacancy) открыл последний {counter}-й тред')
                    break

            #start threads from threads list publicate
            for thread in threads_list_publicate:
                thread.start()
            #start threads from threads list badorgood
            for thread in threads_list_badorgood:
                thread.start()

            #reception of results list from .join
            for thread in threads_list_publicate:
                result = thread.join()
                publicates_list.append(result)

            for thread in threads_list_badorgood:
                result = thread.join()
                bads_or_goods_list.append(result)

            #вычисление не попавших в треды урлов
            #и обработка остатка в одном потоке, ксли такие есть
            if counter < len(urls_list):
                print(f'====MIXIN_GLOBAL_PARSE_HTML (vacancy) отправил в один поток {len(urls_list) - counter} урлов')
                for url_number in range(counter, len(urls_list)):
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (vacancy) обработка {url_number}-го урла')
                    url_strip = urls_list[url_number].strip()
                    publicates_list.append(parse_vacancy_publicate(url_strip))
                    bads_or_goods_list.append(parse_bad_vacancy(url_strip))

            okay = time()
            restime = okay - start
            print(f'====MIXIN_GLOBAL_PARSE_HTML (vacancy) спарсил всё, кроме тегов за: {restime} и {self.threads} тредов')
            
            for item in range(len(titles_list)):
                objects_dict[f'vacancy_{str(item)}'] = {
                                                                'title': titles_list[item],
                                                                'company': companies_list[item],
                                                                'compensation': compensations_list[item],
                                                                'publicate': publicates_list[item],
                                                                'status': bads_or_goods_list[item],
                                                                'url': urls_list[item]
                                                                }
#######################################################################################

#####################################RESUME############################################
        elif self.key_word == 'resume':

            from parserapp.utils import parse_resume_education
            start = time()
            #creating a threads lists for 2 funcs
            counter = 0

            for url in urls_list:
                if counter <= self.threads:
                    url_strip = url.strip()
                    thread = ThreadWithReturn(target=parse_resume_education, args=( url_strip, ))
                    threads_list_education.append(thread)
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (resume) открыл {counter}-й тред')
                    counter += 1
                else:
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (resume) открыл последний {counter}-й тред')
                    break

            #start threads from threads list publicate
            for thread in threads_list_education:
                thread.start()

            for thread in threads_list_education:
                result = thread.join()
                educations_list.append(result)

            #вычисление не попавших в треды урлов
            #и обработка остатка в одном потоке, ксли такие есть
            if counter < len(urls_list):
                print(f'====MIXIN_GLOBAL_PARSE_HTML (resume) отправил в один поток {len(urls_list) - counter} урлов')
                for url_number in range(counter, len(urls_list)):
                    print(f'====MIXIN_GLOBAL_PARSE_HTML (resume) обработка {url_number}-го урла')
                    url_strip = urls_list[url_number].strip()
                    educations_list.append(parse_resume_education(url_strip))

            okay = time()
            restime = okay - start
            print(f'====MIXIN_GLOBAL_PARSE_HTML (resume) спарсил всё, кроме тегов за: {restime} и {self.threads} тредов')

            for item in range(len(urls_list)):
                objects_dict[f'resume_{str(item)}'] = {
                                                                'title': titles_list[item],
                                                                'exp': exp_list[item],
                                                                'education': educations_list[item],
                                                                'refresh': refreshs_list[item],
                                                                'url': urls_list[item]
                                                                }
######################################################################################

        print(f'====MIXIN_GLOBAL_PARSE_HTML возвращаю в дикте {len(objects_dict)} {self.key_word}')
        return objects_dict


class MixinDetailParseHtml:
    """
    Receives HTML from func get_html -> parse each HTML ->
    -> return objects params in dictionary
    """

    base_url = None
    params = None
    key_word = None # publicate or status or vacs rezs or education

    def parse_html_detail(self):
        ge = MixinGetHtml()
        ge.base_url = self.base_url
        ge.params = self.params
        html = ge.get_html()
        main_block = bs(html, 'lxml')

#####################################PUBLICATE########################################
        if self.key_word == 'publicate':
            try:
                publicate = main_block.find('p', class_='vacancy-creation-time').text
            except Exception as Ex:
                print(f'====publicate parse ERROR: {Ex.args}')
                publicate = '00 00 0000'
            publicate_split = publicate.split()
            publicate_str = f'{publicate_split[2]} {publicate_split[3]} {publicate_split[4]}'
            return publicate_str
######################################################################################

######################################STATUS##########################################
        elif self.key_word == 'status':
            description = main_block.find('div', attrs={'data-qa': 'vacancy-description'})
            description_str = description.text
            words_tuple = ('Высшее', 'высшее')
            description_str_split = description_str.split(',')
            for word in description_str_split:
                if (words_tuple[0] in word) or (words_tuple[1] in word):
                    status = 'В/О'
                    return status
                else:
                    continue
            status = 'без В/О'
            return status
#####################################################################################

#####################################VACS/REZS#######################################
        elif self.key_word == 'vacs':
            try:
                vacs = main_block.find('h1').text
            except Exception as Ex:
                logging.info(f'====exept in {self.key_word} "vacanciesrezumes" {Ex.args}')
                vacs = 'Error (see on the log)'
            
            return vacs

        elif self.key_word == 'rezs':
            try:
                rezumes = main_block.find('h1').text
            except Exception as Ex:
                logging.info(f'====exept in {self.key_word} "vacanciesrezumes" {Ex.args}')
                rezumes = 'Error (see on the log)'

            return rezumes
######################################################################################

#####################################EDUCATION########################################
        elif self.key_word == 'education':
            block = main_block.find('div', attrs={'data-qa': 'resume-block-education'})
            try:
                education_title = block.find('span', attrs={'class': 'resume-block__title-text resume-block__title-text_sub'})
                education = education_title.text
            except Exception as Ex:
                print(f'====education parse ERROR: {Ex.args}')
                education = 'Null'
            return education
######################################################################################


class MixinUnpack:
    """
    Unpack dictionary with vacancies into lists
    """

    objects_dict = None
    key_word = None # vacancy or resume

    def unpack_dict(self):
        pprint(f'====MIXIN_UNPACK [START]')

        nums = list()
        titles = list()
        companies = list()
        compensations = list()
        publicates = list()
        statuss = list()
        exps = list()
        educations = list()
        refreshs = list()
        urls = list()
        tags = list()
        counts = list()

        pprint(f'====MIXIN_UNPACK распаковываю дикт в тупл')
#####################################VACANCY##########################################
        if self.key_word == 'vacancy':
            for number, obj in enumerate(self.objects_dict.keys(), 1):
                vacancy_params = self.objects_dict[obj]
                nums.append(f'{number}')
                titles.append(vacancy_params['title'])
                urls.append(vacancy_params['url'])
                companies.append(vacancy_params['company'])
                compensations.append(vacancy_params['compensation'])
                publicates.append(vacancy_params['publicate'])
                statuss.append(vacancy_params['status'])

            nums_sort = sorted(nums, key=len)
            res_tuple = zip(nums_sort, titles, urls, companies, compensations, publicates, statuss)

            pprint(f'====MIXIN_UNPACK распаковал, даю выхлоп res_tuple {self.key_word}')
            pprint(f'====MIXIN_UNPACK [STOP]')
            return res_tuple
#####################################################################################

#####################################RESUME##########################################
        elif self.key_word == 'resume':
            for number, obj in enumerate(self.objects_dict.keys(), 1):
                resume_params = self.objects_dict[obj]
                nums.append(f'{number}')
                titles.append(resume_params['title'])
                urls.append(resume_params['url'])
                exps.append(resume_params['exp'])
                educations.append(resume_params['education'])
                refreshs.append(resume_params['refresh'])

            nums_sort = sorted(nums, key=len)
            res_tuple = zip(nums_sort, titles, urls, exps, educations, refreshs)

            pprint(f'====MIXIN_UNPACK распаковал, даю выхлоп res_tuple {self.key_word}')
            pprint(f'====MIXIN_UNPACK [STOP]')
            return res_tuple
####################################################################################



class MixinSaveToDb:

    key_word = None # vacancy or resume
    tupl = None

    def save_to_db(self):
        pprint(f'====SAVE_TO_DB {self.key_word} [START]')

######################################VACANCY#######################################
        if self.key_word == 'vacancy':
            for number, title, url, company, compensation, date_publicate, status in self.tupl:
                pa = PaVacancies()
                pa.number=number
                pa.title=title
                pa.url=url
                pa.company=company
                pa.compensation=compensation
                pa.date_publicate=date_publicate
                pa.status=status
                pa.save()
#####################################################################################

######################################RESUME#########################################
        elif self.key_word == 'resume':
            for number, title, url, exp, educate, refresh in self.tupl:
                pa = PaResumes()
                pa.number=number
                pa.title=title
                pa.url=url
                pa.exp=exp
                pa.educate=educate
                pa.refresh=refresh
                pa.save()
#####################################################################################

        pprint(f'====SAVE_TO_DB {self.key_word} [STOP]')
        return


class MixinCleanDb:

    key_word = None # resume or vacncy

    def cleaning_db(self):
        pprint(f'====CLANING_DB [START]')

        if self.key_word == 'vacancy':
            pprint(f'====CLANING_DB mode {self.key_word}')
            items = PaVacancies.objects.all()

        elif self.key_word == 'resume':
            pprint(f'====CLANING_DB mode {self.key_word}')
            items = PaResumes.objects.all()

        items.delete()
        pprint(f'====CLANING_DB [STOP]')
        return


class MixinReadFromDb:

    key_word = None # vacancy or resume
    request = None
    show_items = None

    def read_from_db(self):
        pprint(f'====READ_FROM_DATABASE [START]')
        if self.key_word == 'vacancy':
            pprint(f'====READ_FROM_DATABASE mode {self.key_word}')
            items = PaVacancies.objects.all().order_by('number')
        elif self.key_word == 'resume':
            pprint(f'====READ_FROM_DATABASE mode {self.key_word}')
            items = PaResumes.objects.all().order_by('number')
        
        paginator = Paginator(items, self.show_items)
        page_num = self.request.GET.get('page', 1)
        page = paginator.get_page(page_num)
        is_paginated = page.has_other_pages() #если есть другие страницы True else False
        if page.has_previous():
            prev_url = f'?page={page.previous_page_number()}'
        else:
            prev_url = ''
        if page.has_next():
            next_url = f'?page={page.next_page_number()}'
        else:
            next_url = ''
        context={
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
        }

        pprint(f'====READ_FROM_DATABASE [STOP]')
        return context
