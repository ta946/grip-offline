from __future__ import print_function, unicode_literals

from abc import ABCMeta, abstractmethod

from .vendor.six import add_metaclass
from .md_to_html import MarkdownCompiler


@add_metaclass(ABCMeta)
class ReadmeRenderer(object):
    """
    Renders the Readme.
    """
    def __init__(self, user_content=None, context=None):
        if user_content is None:
            user_content = False
        super(ReadmeRenderer, self).__init__()
        self.user_content = user_content
        self.context = context

    @abstractmethod
    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        pass


class GitHubRenderer(ReadmeRenderer):
    pass


class OfflineRenderer(ReadmeRenderer):
    """
    Renders the specified Readme locally using pure Python.

    Note: This is currently an incomplete feature.
    """
    def __init__(self, user_content=None, context=None):
        super(OfflineRenderer, self).__init__(user_content, context)
        self._renderer = MarkdownCompiler(embed_css=False)

    def render(self, text, auth=None):
        """
        Renders the specified markdown content and embedded styles.
        """
        return self._renderer.convert_markdown(text)
