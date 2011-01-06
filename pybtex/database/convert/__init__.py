# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""convert bibliography database from one format to another
"""
from os import path
from pybtex.exceptions import PybtexError
from pybtex.plugin import find_plugin

class ConvertError(PybtexError):
    pass


def convert(from_filename, to_filename,
        from_format=None, to_format=None,
        input_encoding=None, output_encoding=None,
        parser_options=None):
    if parser_options is None:
        parser_options = {}
    input_format = find_plugin('pybtex.database.input', name=from_format, filename=from_filename)
    output_format = find_plugin('pybtex.database.output', name=to_format, filename=to_filename)
    
    if from_filename == to_filename:
        raise ConvertError('input and output file can not be the same')

    bib_data = input_format(input_encoding, **parser_options).parse_file(from_filename)
    output_format(output_encoding).write_file(bib_data, to_filename)
