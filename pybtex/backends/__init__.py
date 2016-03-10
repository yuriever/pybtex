# Copyright (c) 2006-2016  Andrey Golovizin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pybtex.io
from pybtex.plugin import Plugin


class BaseBackend(Plugin):
    """This is the base class for the backends. We encourage
    you to implement as many of the symbols and tags as
    possible when you create a new plugin.

    symbols[u'ndash']    : Used to separate pages
    symbols[u'newblock'] : Used to separate entries in the bibliography
    symbols[u'nbsp']     : A non-breakable space

    tags[u'em']          : emphasize text
    tags[u'strong']      : emphasize text even more
    tags[u'i']           : italicize text, not semantic
    tags[u'b']           : embolden text, not semantic
    tags[u'tt']          : typewrite text, not semantic
    """

    RenderType = basestring  #: the result of render and render_sequence
    default_suffix = None  #: the default suffix for an output file

    def __init__(self, encoding=None):
        self.encoding = encoding or pybtex.io.get_default_encoding()

    def write_prologue(self):
        pass

    def write_epilogue(self):
        pass

    def format_str(self, str_):
        """Format the given string *str_*.
        The default implementation simply returns the string ad verbatim.
        Override this method for non-string backends.
        """
        return str_

    def format_tag(self, tag_name, text):
        """Format a tag with some text inside.

        *tag_name* is a str, and *text* is a rendered Text object.
        """

        raise NotImplementedError

    def format_href(self, url, text):
        """Format a hyperlink with some text inside.

        *url* is a str, and *text* is a rendered Text object.
        """

        raise NotImplementedError

    def format_protected(self, text):
        """Format a "protected" piece of text.

        In LaTeX backend, it is formatted as a {braced group}.
        Most other backends would just output the text as-is.
        """

        return text

    def render_sequence(self, rendered_list):
        """Render a sequence of rendered Text objects.
        The default implementation simply concatenates
        the strings in rendered_list.
        Override this method for non-string backends.
        """
        return "".join(rendered_list)

    def write_entry(self, label, key, text):
        raise NotImplementedError

    def write_to_file(self, formatted_entries, filename):
        with pybtex.io.open_unicode(filename, "w", self.encoding) as stream:
            self.write_to_stream(formatted_entries, stream)
            if hasattr(stream, 'getvalue'):
                return stream.getvalue()

    def write_to_stream(self, formatted_bibliography, stream):
        self.output = stream.write
        self.formatted_bibliography = formatted_bibliography

        self.write_prologue()
        for entry in formatted_bibliography:
            self.write_entry(entry.key, entry.label, entry.text.render(self))
        self.write_epilogue()
