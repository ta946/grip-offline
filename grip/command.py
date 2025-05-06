"""\
grip.command
~~~~~~~~~~~~

Implements the command-line interface for Grip.


Usage:
  grip [options] [<path>] [<address>]
  grip -V | --version
  grip -h | --help

Where:
  <path> is a file to render or a directory containing README.md (- for stdin)
  <address> is what to listen on, of the form <host>[:<port>], or just <port>

Options:
  --user-content        Render as user-content like comments or issues.
  --context=<repo>      The repository context, only taken into account
                        when using --user-content.
  --wide                Renders wide, i.e. when the side nav is collapsed.
                        This only takes effect when --user-content is used.
  --clear               Clears the cached styles and assets and exits.
  --export              Exports to <path>.html or README.md instead of
                        serving, optionally using [<address>] as the out
                        file (- for stdout).
  --renderer=<renderer> Choose the renderer,
                        github: for github style rendering using cmark.
                        commonmark: for vanilla markdown using cmark.
                        markdownpreview: fallback if cmark unavailable, renders github-flavoured markdown.
  -b --browser          Open a tab in the browser after the server starts.
  --title=<title>       Manually sets the page's title.
                        The default is the filename.
  --norefresh           Do not automatically refresh the Readme content when
                        the file changes.
  --quiet               Do not print to the terminal.
  --theme=<theme>       Theme to view markdown file (light mode or dark mode).
                        Valid options ("light", "dark"). Default: "light"
"""

from __future__ import print_function

import sys
import mimetypes
import socket
import errno

from docopt import docopt
from path_and_address import resolve, split_address

from . import __version__
from .api import clear_cache, export, serve
from .exceptions import ReadmeNotFoundError
from .renderers import CMARK_AVAILABLE, VALID_RENDERER_OPTIONS


usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
version = 'Grip ' + __version__

# Note: GitHub supports more than light mode and dark mode (exp: light-high-constrast, dark-high-constrast).
VALID_THEME_OPTIONS = ['light', 'dark']


def main(argv=None, force_utf8=True, patch_svg=True):
    """
    The entry point of the application.
    """
    if force_utf8 and sys.version_info[0] == 2:
        reload(sys)  # noqa
        sys.setdefaultencoding('utf-8')
    if patch_svg and sys.version_info[0] == 2 and sys.version_info[1] <= 6:
        mimetypes.add_type('image/svg+xml', '.svg')

    if argv is None:
        argv = sys.argv[1:]

    # Parse options
    args = docopt(usage, argv=argv, version=version)
    # Handle printing version with -V (docopt handles --version)
    if args['-V']:
        print(version)
        return 0

    # Clear the cache
    if args['--clear']:
        clear_cache()
        return 0

    # Parse theme argument
    if args['--theme']:
        if args['--theme'] in VALID_THEME_OPTIONS:
            theme: str = args['--theme']
        else:
            print('Error: valid options for theme argument are "light", "dark"')
            return 1
    else:
        theme = 'light'

    # Parse renderer argument
    if args['--renderer']:
        renderer = args['--renderer'].lower()
        if renderer in VALID_RENDERER_OPTIONS:
            if CMARK_AVAILABLE:
                renderer: str = renderer
            else:
                print('fallback to MarkdownPreview renderer')
                renderer = 'github'
        else:
            valid_options = '", "'.join(VALID_RENDERER_OPTIONS)
            print(f'Error: valid options for renderer argument are {valid_options}')
            return 1
    else:
        renderer = 'github'

    # Export to a file instead of running a server
    if args['--export']:
        try:
            export(args['<path>'], args['--user-content'], args['--context'],
                   None, None, renderer, args['--wide'],
                   True, args['<address>'],
                   None, args['--title'], args['--quiet'], theme)
            return 0
        except ReadmeNotFoundError as ex:
            print('Error:', ex)
            return 1

    # Parse arguments
    path, address = resolve(args['<path>'], args['<address>'])
    host, port = split_address(address)

    # Validate address
    if address and not host and port is None:
        print('Error: Invalid address', repr(address))

    # Run server
    try:
        serve(path, host, port, args['--user-content'], args['--context'],
              None, None, renderer, args['--wide'], False,
              None, args['--title'], not args['--norefresh'],
              args['--browser'], args['--quiet'], theme, None)
        return 0
    except ReadmeNotFoundError as ex:
        print('Error:', ex)
        return 1
    except socket.error as ex:
        print('Error:', ex)
        if ex.errno == errno.EADDRINUSE:
            print('This port is in use. Is a grip server already running? '
                  'Stop that instance or specify another port here.')
        return 1
