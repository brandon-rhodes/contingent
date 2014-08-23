"""Render a directory of blog posts as HTML."""

import os
import re
from IPython.nbconvert import HTMLExporter
from IPython.nbformat import current as nbformat
from docutils.core import publish_doctree, publish_parts
from docutils import nodes
from glob import glob
from jinja2 import DictLoader

dl = DictLoader({'full.tpl': """\
{%- extends 'display_priority.tpl' -%}
{% block input scoped %}<pre>{{ cell.input }}</pre>
{% endblock %}
{% block pyout scoped %}<pre>{{ output.text | ansi2html }}</pre>
{% endblock %}
{% block markdowncell scoped %}{{ cell.source  | markdown2html }}
{% endblock %}
"""})

def read_text_file(call, path):
    with open(path) as f:
        return f.read()

def parse(call, path):
    source = call(read_text_file, path)
    if path.endswith('.rst'):
        doctree = publish_doctree(source)
        docinfos = doctree.traverse(nodes.docinfo)
        docinfo = {c.tagname: str(c.children[0])
                   for i in docinfos for c in i.children}
        parts = publish_parts(source, writer_name='html')
        return {'body': parts['body'],
                'date': docinfo['date'],
                'title': parts['title']}
    elif path.endswith('.ipynb'):
        notebook = nbformat.reads_json(source)
        exporter = HTMLExporter(config=None, extra_loaders=[dl])
        body, resources = exporter.from_notebook_node(notebook)
        return {'body': body,
                'date': notebook['metadata']['date'],
                'title': notebook['metadata']['name']}

def title_of(call, path):
    info = call(parse, path)
    return info['title']

def date_of(call, path):
    info = call(parse, path)
    return info['date']

def body_of(call, path):
    info = call(parse, path)
    dirname = os.path.dirname(path)
    body = info['body']
    def format_title_reference(match):
        filename = match.group(1)
        title = title_of(call, os.path.join(dirname, filename))
        return '<i>{}</i>'.format(title)
    body = re.sub(r'title_of\(([^)]+)\)', format_title_reference, body)
    return body

def render(call, path):
    return '<h1>{}</h1>\n<p>Date: {}</p>\n{}'.format(
        call(title_of, path), call(date_of, path), call(body_of, path))

def main():
    thisdir = os.path.dirname(__file__)
    indir = os.path.normpath(os.path.join(thisdir, '..', 'posts'))
    outdir = os.path.normpath(os.path.join(thisdir, '..', 'output'))
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    def call(f, *args):
        return f(call, *args)

    paths = (glob(os.path.join(indir, '*.rst')) +
             glob(os.path.join(indir, '*.ipynb')))
    posts = [(call(date_of, path), call(render, path)) for path in paths]
    for post_date, html in sorted(posts):
        print '-' * 72
        print html

if __name__ == '__main__':
    main()
