from __future__ import print_function, unicode_literals

from abc import ABCMeta, abstractmethod

from .vendor.six import add_metaclass
from .md_to_html import MarkdownCompiler

try:
    import cmarkgfm
    CMARK_AVAILABLE = True
except:
    CMARK_AVAILABLE = False

VALID_RENDERER_OPTIONS = ['github', 'markdownpreview', 'commonmark']


def get_renderer(renderer, user_content, context):
    if renderer == 'github':
        renderer = GitHubRenderer(user_content, context)
    elif renderer == 'commonmark':
        renderer = CommonMarkRenderer(user_content, context)
    else:
        renderer = OfflineRenderer(user_content, context)
    return renderer

@add_metaclass(ABCMeta)
class ReadmeRenderer:
    """
    Renders the Readme.
    """
    def __init__(self, user_content=None, context=None):
        if user_content is None:
            user_content = False
        self.user_content = user_content
        self.context = context

    @abstractmethod
    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        pass


class CommonMarkRenderer(ReadmeRenderer):
    """
    Renders the specified Readme as normal CommonMark using github's cmark renderer
    """
    def __init__(self, user_content=None, context=None):
        super().__init__(user_content, context)

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        return cmarkgfm.markdown_to_html(text)


class GitHubRenderer(ReadmeRenderer):
    """
    Renders the specified Readme as Github Markdown using github's cmark renderer
    """
    def __init__(self, user_content=None, context=None):
        super().__init__(user_content, context)

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        return cmarkgfm.github_flavored_markdown_to_html(text)


class OfflineRenderer(ReadmeRenderer):
    """
    Renders the specified Readme as Github-Falvoured (approximation) Markdown using pure Python.
    """
    def __init__(self, user_content=None, context=None):
        super().__init__(user_content, context)
        self._renderer = MarkdownCompiler(embed_css=False)

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        return self._renderer.convert_markdown(text)
