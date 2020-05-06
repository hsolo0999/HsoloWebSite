from .constants import Const
import sys
from pprint import pprint
from time import time
from parserapp.mixindef import MixinGetHtml, MixinGlobalParseHtml, MixinDetailParseHtml , MixinUnpack, MixinSaveToDb, MixinCleanDb, MixinReadFromDb


class GetHTML(MixinGetHtml):
    base_url = None
    params = None


class ParseGlobal(MixinGlobalParseHtml):
    #show_items = None
    threads = None
    base_url = None
    params = None
    key_word = None # resume or vacancy


class ParseDetail(MixinDetailParseHtml):
    base_url = None
    params = None
    key_word = None # publicate or status or vacs rezs or tags or education


class Unpack(MixinUnpack):
    objects_dict = None
    key_word = None # vacancy or resume


class SaveDb(MixinSaveToDb):
    key_word = None # vacancy or resume


class CleanDb(MixinCleanDb):
    key_word = None # resume or vacncy


class ReadDb(MixinReadFromDb):
    key_word = None # vacancy or resume
    request = None
    show_items = None



def parse_html_vacancies(settings):
    gparse = ParseGlobal()
    #gparse.show_items = settings.show_items
    gparse.threads = settings.threads
    gparse.base_url = settings.url_base
    gparse.params = {
                'page': settings.page,
                'area': settings.region,
                'text': settings.query,
                }
    gparse.key_word = 'vacancy'
    vacancies_dict = gparse.parse_html()

    unpack = Unpack()
    unpack.objects_dict = vacancies_dict
    unpack.key_word = 'vacancy'
    result = unpack.unpack_dict()

    return result


def parse_html_resumes(settings):
    gparse = ParseGlobal()
    #gparse.show_items = settings.show_items
    gparse.threads = settings.threads
    gparse.base_url = settings.url_base
    gparse.params = {
                'page': settings.page,
                'area': settings.region,
                'text': settings.query,
                }
    gparse.key_word = 'resume'
    resumes_dict = gparse.parse_html()

    unpack = Unpack()
    unpack.objects_dict = resumes_dict
    unpack.key_word = 'resume'
    result = unpack.unpack_dict()

    return result


def parse_resume_education(resume_url):
    parse = ParseDetail()
    parse.base_url = resume_url
    parse.key_word = 'education'
    result = parse.parse_html_detail()

    return result


def parse_vacancy_publicate(vacancy_url):
    """
    Receives input vacancy url -> receives HTML from func get_html_vacancy ->
    parse each HTML -> return date of publication as string
    """
    parse = ParseDetail()
    parse.base_url = vacancy_url
    parse.key_word = 'publicate'
    result = parse.parse_html_detail()

    return result


def parse_bad_vacancy(vacancy_url):
    """
    Receives input vacancy url -> receives HTML from func get_html_vacancy ->
    parse each HTML -> return TRUE if words include in the vacancy description ->
    else return False
    """
    parse = ParseDetail()
    parse.base_url = vacancy_url
    parse.key_word = 'status'
    result = parse.parse_html_detail()

    return result


def parse_vacsrezumes(settings):
    """
    Determines the total number of vacancies and resumes
    """
    parse = ParseDetail()
    parse.base_url = Const.url_base
    parse.params = {
                    'area': settings.region,
                    'text': settings.query,
                    }
    parse.key_word = 'vacs'
    vacs = parse.parse_html_detail()

    parse.base_url = Const.url_base_resume
    parse.params = {
                    'area': settings.region,
                    'text': settings.query,
                    }
    parse.key_word = 'rezs'
    rezs = parse.parse_html_detail()

    return vacs, rezs


def save_db(tupl, key_word):
    pprint(f'===SAVEDB mode {key_word}')
    sav = SaveDb()
    sav.key_word = key_word
    sav.tupl = tupl
    sav.save_to_db()
    return


def clean_db(key_word):
    pprint(f'===CLAENDB mode {key_word}')
    clean = CleanDb()
    clean.key_word = key_word
    clean.cleaning_db()
    return


def read_db(request, settings, key_word):
    pprint(f'===READDB mode {key_word}')
    read = ReadDb()
    read.key_word = key_word
    read.request = request
    read.show_items = settings.show_items
    context = read.read_from_db()
    return context