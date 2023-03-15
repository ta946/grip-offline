import os
import html

import markdown
import markdown.extensions
import pymdownx.superfences
import pymdownx.emoji
from pymdownx.pathconverter import PathConverterPostprocessor
from pymdownx.b64 import B64Postprocessor


def slugify_bitbucket(*args, **kwargs):
    """convert header id to bitbucket syntax"""
    text = markdown.extensions.toc.slugify(*args, **kwargs)
    text = 'markdown-header-{}'.format(text)
    return text


MARKDOWN_EXTENSIONS = [
    'markdown.extensions.footnotes',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.tables',
    'markdown.extensions.abbr',
    'markdown.extensions.md_in_html',
    'pymdownx.betterem',
    {
        'markdown.extensions.toc': {
                                    'permalink': '\ue157',
                                    'slugify': slugify_bitbucket
                                    }
    },
    'markdown.extensions.meta',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
    'markdown.extensions.wikilinks',
    'markdown.extensions.admonition',
    # PyMdown extensions that help give a GitHub-ish feel
    {
        'pymdownx.superfences': {  # Nested fences and UML support
            'custom_fences': [
                {
                    'name': 'flow',
                    'class': 'uml-flowchart',
                    'format': pymdownx.superfences.fence_code_format
                },
                {
                    'name': 'sequence',
                    'class': 'uml-sequence-diagram',
                    'format': pymdownx.superfences.fence_code_format
                },
                {
                    'name': 'mermaid',
                    'class': 'mermaid',
                    'format': pymdownx.superfences.fence_code_format
                }
            ]
        }
    },
    {
        'pymdownx.magiclink': {   # Auto linkify URLs and email addresses
            'repo_url_shortener': True,
            'repo_url_shorthand': True
        }
    },
    'pymdownx.tasklist',     # Task lists
    {
        'pymdownx.tilde': {  # Provide ~~delete~~
            'subscript': False
        }
    },
    {
        'pymdownx.emoji': {  # Provide GitHub's emoji
            'emoji_index': pymdownx.emoji.gemoji,
            'emoji_generator': pymdownx.emoji.to_png,
            'alt': 'short',
            'options': {
                'attributes': {
                    'align': 'absmiddle',
                    'height': '20px',
                    'width': '20px'
                },
                'image_path': 'https://github.githubassets.com/images/icons/emoji/unicode/',
                'non_standard_image_path': 'https://github.githubassets.com/images/icons/emoji/'
            }
        }
    }
]


class MarkdownCompiler:
    """Python Markdown compiler."""
    compiler_name = 'markdown'

    def __init__(self, convert_images_to_base64=None, embed_css=None):
        self._convert_images_to_base64 = bool(convert_images_to_base64) if convert_images_to_base64 is not None else False
        self._embed_css = bool(embed_css) if embed_css is not None else True
        self._file_path = None
        self._base_path = ''
        self._css_path = None
        self._css_text = self.get_default_css()
        self._pygments_css_path = None
        self._pygments_style = self.set_highlight('github', 'highlight')
        extensions, extension_configs = self.get_config_extensions()
        self._md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        self._pathconv = PathConverterPostprocessor()
        self._b64proc = B64Postprocessor() if self._convert_images_to_base64 else None

    def get_default_css(self):
        css_path = os.path.abspath(os.path.join(__file__,'..','static','markdown.css'))
        self._css_path = css_path
        with open(css_path,'r') as f:
            css_txt = f.read()
        css_text = '<style>{}</style>'.format(css_txt)
        return css_text

    def set_highlight(self, pygments_style, css_class):
        """Set the Pygments CSS."""
        pygments_css_path = os.path.abspath(os.path.join(__file__,'..','static','pygments_{}.css'.format(pygments_style)))
        self._pygments_css_path = pygments_css_path
        with open(pygments_css_path, 'r') as f:
            css_text = f.read()
        style = css_text % {
            'css_class': ''.join(['.' + x for x in css_class.split(' ') if x])
        }
        pygments_style = '<style>%s</style>' % style
        return pygments_style

    def process_extensions(self, extensions):
        """Process extensions and related settings."""
        names = []
        settings = {}
        for e in extensions:
            # Ensure extension is in correct format and separate config from extension
            if isinstance(e, str):
                ext = e
                config = {}
            elif isinstance(e, dict):
                ext = list(e.keys())[0]
                config = list(e.values())[0]
                if config is None:
                    config = {}
            else:
                continue
            names.append(ext)
            settings[ext] = config
        return names, settings

    def get_config_extensions(self):
        """Get the extensions to include from the settings."""
        return self.process_extensions(MARKDOWN_EXTENSIONS)

    def parser_specific_convert(self, markdown_text):
        """Parse Markdown with Python Markdown."""
        html_text = self._md.convert(markdown_text)
        return html_text

    def postprocessor_pathconverter(self, source, image_convert, file_convert, absolute=False):
        """Convert paths to absolute paths."""
        relative_path = ''
        tags = []
        if file_convert:
            tags.extend(['script', 'a', 'link'])
        if image_convert:
            tags.append('img')
        self._pathconv.config = {
            'base_path': self._base_path,
            'relative_path': relative_path,
            'absolute': absolute,
            'tags': ' '.join(tags)
        }
        return self._pathconv.run(source)

    def postprocessor_base64(self, source):
        """Convert resources (currently images only) to base64."""
        self._b64proc.config = {'base_path': self._base_path}
        return self._b64proc.run(source)

    def convert_markdown(self, markdown_text):
        """Convert input markdown to HTML, with GitHub, GitLab or builtin parser."""
        markdown_html = self.parser_specific_convert(markdown_text)
        markdown_html = self.postprocessor_pathconverter(markdown_html, image_convert=True, file_convert=True, absolute=True)
        if self._convert_images_to_base64:
            markdown_html = self.postprocessor_base64(markdown_html)
        return markdown_html

    def get_highlight(self):
        """Return the Pygments CSS if enabled."""
        return self._pygments_style if self._pygments_style else ''

    def get_title(self):
        """Get HTML title."""
        if self._file_path is not None:
            title = os.path.splitext(os.path.basename(self._file_path))[0]
        else:
            title = 'untitled'
        return '<title>%s</title>' % html.escape(title)

    def run(self, contents, file_path=None):
        """Return full HTML and body HTML for view."""
        self._file_path = file_path
        self._base_path = os.path.dirname(self._file_path) if self._file_path is not None else None

        body = self.convert_markdown(contents)

        html_txt = '<!DOCTYPE html>'
        html_txt += '<html><head><meta charset="utf-8">'
        html_txt += '<meta name="viewport" content="width=device-width, initial-scale=1">'
        if self._embed_css:
            html_txt += self._css_text
            html_txt += self.get_highlight()
        html_txt += self.get_title()
        html_txt += '</head><body>'
        html_txt += '<article class="markdown-body" id="md2html_0">'
        html_txt += body
        html_txt += '</article>'
        html_txt += '</body>'
        html_txt += '</html>'

        return html_txt, body
