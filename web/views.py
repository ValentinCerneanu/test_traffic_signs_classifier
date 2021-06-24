from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.template import loader

from .forms import MyForm

class FormView(View):
    def get(self, request):
        template = loader.get_template('form.html')
        context = {}

        context['form'] = MyForm()

        return render(request, 'form.html', context)

    def post(self, request):
        context = {}
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image")
            print(img)
            print(name)

            form.save()

        context['name'] = name

        return render(request, 'form.html', context)