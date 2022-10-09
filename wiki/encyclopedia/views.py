from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import Http404
from . import util
import urllib3
from django.core.files.storage import default_storage
from django.http import JsonResponse
import markdown2



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/entries.html", {
            "entries":  markdown2.markdown(util.get_entry(title)),
            "entry_title": title
        })


def create(request):
    if request.method == "POST":
        filename = f"entries/{request.POST['entry_name']}.md"
        if default_storage.exists(filename):
            return render(request, "encyclopedia/already_exst.html", {})
        else:
            entryname = request.POST['entry_name']
            util.save_entry(request.POST["entry_name"], request.POST["entry_content"])
            return redirect(f'/{entryname}')
    else:
        return render(request, "encyclopedia/create.html", {})


def random(request):
    title = util.random_entry()
    return render(request, "encyclopedia/entries.html", {
        "entries": markdown2.markdown(util.get_entry(title)),
        "entry_title": title
    })


def search(request):
        search_results = request.GET.get('q', '')
        http = urllib3.PoolManager()
        error = http.request("GET", "http://127.0.0.1:8000/" + search_results)
        if (error.status == 404):
            print("Error404...running substring")
            return render(request, "encyclopedia/index.html", {
        "entries": util.search_substring(search_results)
    })
        else:
            return redirect(f'/{search_results}')
   

def edit(request, title):
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/entries_edit.html", {
        "entries": entry,
        "entry_title": title
        })
    else:
        entry_title = request.POST["entry_title"]
        content = request.POST["content"]
        util.save_entry(entry_title, content)
        return redirect(f'/{entry_title}')
