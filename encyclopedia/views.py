from faulthandler import disable
from hashlib import new
from logging import PlaceHolder
from multiprocessing import context
from tkinter import DISABLED
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice

from . import util


class NewPageForm(forms.Form):
    statiaHead = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Page title. Please enter in English only'}
    ))
    statiaBody = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Page text in Markdown style. Please enter in English only'}
    ))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def statia(request, statia):
    markdownpage = Markdown()
    page = util.get_entry(statia)
    if page is None:
        return render (request, "encyclopedia/fileNoneExist.html", {
        "statiaHead": statia
    })
    else:
        return render (request,"encyclopedia/statia.html", {
        "statia": markdownpage.convert(page),
        "statiaHead": statia
    })

def edit_page(request, statiaHead):
    statiaBody =util.get_entry(statiaHead)
    form = NewPageForm()
    form.fields['statiaHead'].initial = statiaHead
    form.fields['statiaBody'].initial = statiaBody
    form.fields['statiaHead'].widget = forms.HiddenInput()
    if request.method == "POST":
        statiaHead = request.POST['statiaHead']
        statiaBody = request.POST['statiaBody']
        util.save_entry(statiaHead, statiaBody)
        return HttpResponseRedirect(reverse("encyclopedia:statia", kwargs={'statia': statiaHead}))
    return render (request,"encyclopedia/new_statia.html", {
                "form": form,
                "edit": True,
                "statiaHead": form.fields['statiaHead'].initial
    })

def new_statia(request):
    markdownpage = Markdown()
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
           statiaHead=form.cleaned_data['statiaHead']
           statiaBody=form.cleaned_data['statiaBody']
           if statiaHead in util.list_entries():
                error = "This page is exist. You can find it and change."
                return render(request, "encyclopedia/new_statia.html", {
                    "form": form,
                    "error": error,
                    "edit": False
                })
           else:
               util.save_entry(statiaHead, statiaBody)
               return render (request,"encyclopedia/statia.html", {
                    "statia": markdownpage.convert(statiaBody),
                    "statiaHead": statiaHead
               })
    return render(request, "encyclopedia/new_statia.html", {
        "form": NewPageForm()
    })

def search(request):
    search_page = request.GET.get("q")
    search_list = []
    if util.get_entry(search_page) is not None:
        return HttpResponseRedirect(reverse("encyclopedia:statia", kwargs={"statia": search_page}))
    else:
        search_page_lower = search_page.lower()
        statias = util.list_entries()
        for statia in statias:
           search_cycle = statia.lower().find(search_page_lower)
           if search_cycle != -1:
              search_list.append(statia)
              print(search_list)
        if len(search_list)==0:
            return render (request, "encyclopedia/nonefile.html", {
                "statiaHead": search_page
        })
        else:
             return render (request, "encyclopedia/search.html", {
                "statias": search_list
        })
def random(request):
    statias = util.list_entries()
    statia = choice(statias)
    return HttpResponseRedirect(reverse("encyclopedia:statia", kwargs={'statia': statia}))