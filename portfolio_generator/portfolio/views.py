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


def _handle_title(text, lvl):
    return f"<h{lvl}>{text}</h{lvl}>"

def _handle_code(text, language):
    return f"<p>{text}</p>"

def _parse_line(line):
    if not line:
        return None

    if line[1] == 'title': return _handle_title(line[0], line[2]) + '\n'
    if line[1] == 'text': return line[0] + '\n'
    if line[1] == 'code': return _handle_code(line[0], line[2])+ '\n'

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
    doc = ''
    line = 'content'
    while line:
        line = _parse_line(reader.read_line())

        if line:
            doc += line

    context = {'content': doc}

    return render(request, 'project_preview.html', context)