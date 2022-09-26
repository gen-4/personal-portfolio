from django.shortcuts import render
from django.http import Http404

from os import scandir

from portfolio.utils.readme_reader import Markdown


def get_main_page(request):
    files = []
    projects = []

    with scandir("./python") as entries:
        for entry in entries:
            if entry.is_dir:
                with scandir(entry) as deep_entries:
                    for deep_entry in deep_entries:
                        if deep_entry.name == 'README.md':
                            files.append(deep_entry)

    for file in files:
        reader = Markdown(file.path)
        title = None
        while not title:
            text, clas, arg = reader.read_line()
            if clas == 'title' and arg == '1':
                title = text
        
        projects.append({
            'title': title,
            'url': f'project/{title}'
            })

    context = {
        'projects': projects
    }

    return render(request, 'index.html', context)


def get_project(request, project_name):
    file = None

    with scandir("./python") as entries:
        for entry in entries:
            if entry.is_dir and entry.name == project_name:
                with scandir(entry) as deep_entries:
                    for deep_entry in deep_entries:
                        if deep_entry.name == 'README.md':
                            file = deep_entry

    if not file:
        raise Http404

    reader = Markdown(file.path)
    doc = []
    line = True
    while line:
        text, typ, arg = reader.read_line()
        if typ == 'title': arg = f'h{arg}'
        if typ == 'text': 
            if text == '\n': continue
            
        line = {
            'text': text,
            'type': typ,
            'arg': arg
        }

        if not text:
            line = None
        else:
            doc.append(line)

    context = {'content': doc}

    return render(request, 'project_preview.html', context)