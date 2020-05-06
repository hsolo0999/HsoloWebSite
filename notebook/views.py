from django.shortcuts import render, get_object_or_404, redirect
from .models import NbLine, NbTag
from django.views.generic import View
from .mixins import DetailsMixin, CreateMixin
from .forms import NbTagForm, NbLineForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import random
import pprint


emj_list = ['🖐','🤟','🤘','🤙','😯','🤗','😱','🤓','😋','🙂','😌','🙈','🙊','😁','😄','😃']


def lines_show(request):
    rnd_emj = random.choice(emj_list)
    lines = NbLine.objects.all()
    paginator = Paginator(lines, 3)
    page_num = request.GET.get('page', 1)
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
        'emj': rnd_emj,
    }

    return render(request, 'notebook/lines.html', context=context)

def tags_show(request):
    rnd_emj = random.choice(emj_list)
    tags = NbTag.objects.all()
    return render(request, 'notebook/tags.html', context={'tags': tags, 'emj': rnd_emj})


class NbLineCreate(LoginRequiredMixin, CreateMixin, View):
    form_model = NbLineForm
    form_temp = 'notebook/create_line.html'
    raise_exception = True


class NbTagCreate(CreateMixin, View):
    form_model = NbTagForm
    form_temp = 'notebook/create_tag.html'


class NbLineDetail(DetailsMixin, View):
    model_detail = NbLine
    temp_detail = 'notebook/line_details.html'

    model_edit = NbLine
    model_form_edit = NbLineForm
    temp_edit = 'notebook/line_edit.html'
    raise_exception = True


class NbTagDetail(DetailsMixin, View):
    model_detail = NbTag
    temp_detail = 'notebook/tag_details.html'

    model_edit = NbTag
    model_form_edit = NbTagForm
    temp_edit = 'notebook/tag_edit.html'


class NbLineDelete(View):
    def get(self, request, slug):
        line = NbLine.objects.get(slug__iexact=slug)
        return render(request, 'notebook/line_delete.html', context={'nbline': line})

    def post(self, request, slug):
        line = NbLine.objects.get(slug__iexact=slug)
        line.delete()
        return redirect(reverse('nb_lines_url'))
    
    raise_exception = True


class NbTagDelete(View):
    def get(self, request, slug):
        print(f'1====slug : {slug}')
        tag = NbTag.objects.get(slug__iexact=slug)
        print(f'2====tag -> context nbtag: {tag}')
        return render(request, 'notebook/tag_delete.html', context={'nbtag': tag})

    def post(self, request, slug):
        tag = NbTag.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse('nb_tags_url'))
