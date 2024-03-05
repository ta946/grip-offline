Grip-offline -- Markdown offline rendering server
=====================================

## Forked from [Grip](https://github.com/joeyespo/grip). [Original README](./README_original.md)


Render local markdown files offline.

**Grip-offline** is a command-line server application written in Python that uses 
code taken from SublimeText plugin [MarkdownPreview v2.4.2](https://github.com/facelessuser/MarkdownPreview/releases/tag/st3-2.4.2)
to render local markdown files in your browser and allow you to follow their links. Changes you make to the Readme will be instantly reflected in the browser without requiring a page refresh.


The styles and rendering are a close apporximation to Github's renderer and will not be exactly the same so keep that it mind.

Also, this fork has been modified to work for simple offline rendering only.
The other functionality has not been tested and may not work.




Installation
------------

To install **Grip-offline**:

in terminal, go to the folder where you cloned **Grip-offline** then run

```console
$ pip install .
```


Usage
-----

To render the readme of a repository:

```console
$ cd myrepo
$ grip
 * Running on http://localhost:6419/
```

Now open a browser and visit [http://localhost:6419](http://localhost:6419/).


You can also specify a port, used `--theme="dark"` to render in dark mode and/or use `-b` to automatically open a new browser tab for you.:

```console
$ grip 80 -b --theme="dark"
 * Running on http://localhost:80/
```

Or an explicit file:

```console
$ grip AUTHORS.md
 * Running on http://localhost:6419/
```

Alternatively, you could just run `grip` and visit [localhost:6419/AUTHORS.md](AUTHORS.md)
since grip supports relative URLs.

You can even bypass the server and **export** to a single HTML file, with all the styles and assets inlined:

```console
$ grip --export
Exporting to README.html
```

Control the output name with the second argument:

```console
$ grip README.md --export index.html
Exporting to index.html
```

If you're exporting a bunch of files, you can prevent styles from being inlining to save space with `--no-inline`:

```console
$ grip README.md --export --no-inline introduction.html
Exporting to introduction.html
```

Reading and writing from **stdin** and **stdout** is also supported, allowing you to use Grip with other programs:

```console
$ cat README.md | grip -
 * Running on http://localhost:6419/
```

```console
$ grip AUTHORS.md --export - | bcat
```

```console
$ cat README.md | grip --export - | less
```

This allows you to quickly test how things look by entering Markdown directly in your terminal:

```console
$ grip -
Hello **world**!
^D
 * Running on http://localhost:6419/
```

*Note: `^D` means `Ctrl+D`, which works on Linux and OS X. On Windows you'll have to use `Ctrl+Z`.*

Rendering as user-content like **comments** and **issues** is also supported, with an optional repository context for linking to issues:

```console
$ grip --user-content --context=joeyespo/grip
 * Running on http://localhost:6419/
```

For more details and additional options, see the help:

```console
$ grip -h
```


Configuration
-------------

To customize Grip, create `~/.grip/settings.py`, then add one or more of the following variables:

- `DEBUG`: Whether to use Flask's debugger when an error happens, `False` by default
- `DEBUG_GRIP`: Prints extended information when an error happens, `False` by default
- `CACHE_DIRECTORY`: The directory, relative to `~/.grip`, to place cached assets (this gets run through the following filter: `CACHE_DIRECTORY.format(version=__version__)`), `'cache-{version}'` by default
- `AUTOREFRESH`: Whether to automatically refresh the Readme content when the file changes, `True` by default
- `QUIET`: Do not print extended information, `False` by default



#### Environment variables

- `GRIPHOME`: Specify an alternative `settings.py` location, `~/.grip` by default
- `GRIPURL`: The URL of the Grip server, `/__/grip` by default

#### Advanced

This file is a normal Python script, so you can add more advanced configuration.

For example, to read a setting from the environment and provide a default value
when it's not set:

```python
PORT = os.environ.get('GRIP_PORT', 8080)
```


API
---

You can access the API directly with Python, using it in your own projects:

```python
from grip import serve

serve(port=8080)
 * Running on http://localhost:8080/
```

Run main directly:

```python
from grip import main

main(argv=['-b', '8080'])
 * Running on http://localhost:8080/
```

Or access the underlying Flask application for even more flexibility:

```python
from grip import create_app

grip_app = create_app(user_content=True)
# Use in your own app
```


### Documentation

#### serve

Runs a local server and renders the Readme file located
at `path` when visited in the browser.

```python
serve(path=None, host=None, port=None, user_content=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=False, api_url=None, title=None, autorefresh=True, browser=False, theme='light', grip_class=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `host`: The host to listen on, defaulting to the HOST configuration variable
- `port`: The port to listen on, defaulting to the PORT configuration variable
- `user_content`: Whether to render a document as [user-content][] like user comments or issues
- `context`: The project context to use when `user_content` is true, which
             takes the form of `username/project`
- `username`: Not used. Set to `None`
- `password`: Not used. Set to `None`
- `render_offline`: use SublimeText MarkdownPreview renderer (will break if set to False!)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `user_content`)
- `render_inline`: Whether to inline the styles within the HTML file
- `api_url`: Not used. Set to `None`
- `title`: The page title, derived from `path` by default
- `autorefresh`: Automatically update the rendered content when the Readme file changes, `True` by default
- `browser`: Open a tab in the browser after the server starts., `False` by default
- `grip_class`: Use a custom [Grip class](#class-gripflask)


#### export

Writes the specified Readme file to an HTML file with styles and assets inlined.

```python
export(path=None, user_content=False, context=None, username=None, password=None, render_offline=False, render_wide=False, render_inline=True, out_filename=None, api_url=None, title=None, quiet=None, theme='light', grip_class=None)
```

- `path`: The filename to render, or the directory containing your Readme file, defaulting to the current working directory
- `user_content`: Whether to render a document as [user-content][] like user comments or issues
- `context`: The project context to use when `user_content` is true, which
             takes the form of `username/project`
- `username`: Not used. Set to `None`
- `password`: Not used. Set to `None`
- `render_offline`: use SublimeText MarkdownPreview renderer (will break if set to False!)
- `render_wide`: Whether to render a wide page, `False` by default (this has no effect when used with `user_content`)
- `render_inline`: Whether to inline the styles within the HTML file (Must be set to True!)
- `out_filename`: The filename to write to, `<in_filename>.html` by default
- `api_url`: Not used. Set to `None`
- `title`: The page title, derived from `path` by default
- `quiet`: Do not print to the terminal
- `theme`: Theme to view markdown file (light mode or dark mode). Valid options ("light", "dark"). Default: "light".
- `grip_class`: Use a custom [Grip class](#class-gripflask)
