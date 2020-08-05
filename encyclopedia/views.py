from django.shortcuts import render, redirect
import markdown2
from . import util
from django import forms
from django.core.files.storage import default_storage
import random

# Start of forms


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 1, "cols": "1"}), label="Body"
    )


class EditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="")


# Start of views


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    # Check if page exists if not render and error page.
    if util.get_entry(title) == None:
        return render(
            request, "encyclopedia/error.html", {"error": "Page does not exist."}
        )
    # Gets the proper markdown file and converts it to html.
    else:
        return render(
            request,
            "encyclopedia/entry.html",
            {"content": markdown2.markdown(util.get_entry(title)), "title": title},
        )


def search(request):
    lst = []
    title = request.GET["q"].lower()
    entries = util.list_entries()
    if util.get_entry(title) != None:
        return render(
            request,
            "encyclopedia/entry.html",
            {"content": markdown2.markdown(util.get_entry(title)), "title": title},
        )
    else:
        for entry in entries:
            entry = entry.lower()
            if entry.startswith(title):
                entry = entry.capitalize()
                lst.append(entry)
        if len(lst) > 0:
            return render(request, "encyclopedia/results.html", {"lst": lst})
        else:
            return render(
                request, "encyclopedia/error.html", {"error": "Page does not exist."}
            )


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = markdown2.markdown(content)
            filename = f"entries/{title}.md"
            if default_storage.exists(filename):
                return render(
                    request,
                    "encyclopedia/error.html",
                    {"error": "A file with this title already exists."},
                )
            else:
                util.save_entry(title, content)
                return redirect("entry", title=title)
    else:
        return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})


def edit(request, title):
    if request.method == "GET":
        form = EditEntry()
        page = util.get_entry(title)
        return render(
            request,
            "encyclopedia/edit.html",
            {"edit": EditEntry(initial={"content": page}), "title": title},
        )
    else:
        form = EditEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            page = util.get_entry(title)
            page_converted = markdown2.markdown(page)
            return redirect("entry", title=title)


def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        page_random = entries[num]
        title = util.get_entry(page_random)
        page_converted = markdown2.markdown(title)
        return render(
            request,
            "encyclopedia/entry.html",
            {"content": page_converted, "title": title},
        )
