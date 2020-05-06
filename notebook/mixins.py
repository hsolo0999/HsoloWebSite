from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import os
import random


emj_list = ['🖐','🤟','🤘','🤙','😯','🤗','😱','🤓','😋','🙂','😌','🙈','🙊','😁','😄','😃']


class DetailsMixin:
    model_detail = None
    temp_detail = None

    model_edit = None
    model_form_edit = None
    temp_edit = None

    def get(self, request, slug):
        obj_detail = get_object_or_404(self.model_detail, slug__iexact=slug)
        print(f'====context get(det) {self.model_detail.__name__.lower()} : {obj_detail}')

        obj_edit = self.model_edit.objects.get(slug__iexact=slug)
        edit_form = self.model_form_edit(instance=obj_edit)
        print(f'====context get(edit) {self.model_edit.__name__.lower()} : {obj_edit}')
        print(f'====context get(edit) form : {edit_form}')
        return render(request,
                        self.temp_detail,
                        context={'form': edit_form,
                                self.model_edit.__name__.lower(): obj_edit,
                                self.model_detail.__name__.lower(): obj_detail})

    def post(self, request, slug):
        obj_edit = self.model_edit.objects.get(slug__iexact=slug)
        edit_form = self.model_form_edit(request.POST, request.FILES, instance=obj_edit)

        if edit_form.is_valid():
            if 'img' in request.FILES:
                edit_form.img = request.FILES['img']
            edited_obj = edit_form.save(commit=True)
            print(f'====edited_obj : {edited_obj}')
            return redirect(edited_obj)
        print(f'====context post(edit) {self.model_edit.__name__.lower()} : {obj_edit}')
        print(f'====context post(edit) form : {edit_form}')
        return render(request,
                        self.temp_edit,
                        context={'form': edit_form, self.model_edit.__name__.lower(): obj_edit})


class CreateMixin:
    form_model = None
    form_temp = None

    def get(self, request):
        rnd_emj = random.choice(emj_list)
        get_form = self.form_model
        return render(request, self.form_temp, context={'form': get_form, 'emj': rnd_emj})

    def post(self, request):
        post_form = self.form_model(request.POST, request.FILES)

        if post_form.is_valid():
            if 'img' in request.FILES:
                post_form.img = request.FILES['img']
            new_obj = post_form.save(commit=True)
            return redirect(new_obj)
        else:
            print(f'====ERROR: {post_form.errors}')

        return render(request, self.form_temp, context={'form' : post_form})

class EditMixin:

# class NbLineEdit(LoginRequiredMixin, EditMixin, View):
#     model = NbLine
#     model_form = NbLineForm
#     temp = 'notebook/line_edit.html'
#     raise_exception = True

    model = None
    model_form = None
    temp = None


    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        edit_form = self.model_form(instance=obj)
        return render(request,
                        self.temp,
                        context={'form': edit_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        edit_form = self.model_form(request.POST, request.FILES, instance=obj)

        if edit_form.is_valid():
            if 'img' in request.FILES:
                edit_form.img = request.FILES['img']
            edited_obj = edit_form.save(commit=True)
            return redirect(edited_obj)
        return render(request,
                        self.temp,
                        context={'form': edit_form, self.model.__name__.lower(): obj})
