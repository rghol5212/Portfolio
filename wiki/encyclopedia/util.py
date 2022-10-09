import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import Http404
import os, random
from django.http import HttpResponse


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))



def random_entry():
    entries_list = default_storage.listdir("entries")
    random_entry = random.randrange(len(entries_list[1]))
    filename = entries_list[1][random_entry]
    return filename.rstrip(".md")



def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        raise Http404(title + " Does not exist. Please try again, or create a new page.")



def search_substring(title):
    _, filenames = default_storage.listdir("entries")
    filename_list = list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))
    entry_search = []

    for x in filename_list:
        if str(title.lower()) in str(x.lower()):
            entry_search.append(x)
    
    return entry_search
