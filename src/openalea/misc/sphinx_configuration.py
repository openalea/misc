"""Sphinx conf.py file that is common to all OpenAlea packages"""
# -*- coding: utf-8 -*-
#
# documentation build configuration file, created by
# sphinx-quickstart on Wed Dec  2 17:50:25 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.


import sys, os
import openalea.misc as misc


# figure out where is installed misc so as to get all the sphinx configuration templates, 
# and extensions that can be found in misc/share

#develop mode
openalea = misc.__path__[0] + os.sep +'..' + os.sep + '..' + os.sep + '..' + os.sep +'share' + os.sep
if os.path.isdir(os.path.join(openalea, 'sphinxext')):
    print 'develop mode'
    sys.path.append(os.path.join(openalea,'sphinxext'))
else:
    #install mode
    openalea = misc.__path__[0] + os.sep +'..' + os.sep + '..' + os.sep +'share' + os.sep
    if os.path.isdir(os.path.join(openalea, 'sphinxext')):
        sys.path.append(os.path.join(openalea,'sphinxext'))
    else:
        raise ImportError('could not find the share directory of openalea.misc.')

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc', 
    'sphinx.ext.autosummary', 
    'sphinx.ext.coverage', 
    'sphinx.ext.graphviz',
    'sphinx.ext.doctest', 
    'sphinx.ext.intersphinx', 
    'sphinx.ext.todo', 
    'sphinx.ext.coverage', 
    'sphinx.ext.pngmath', 
    'sphinx.ext.ifconfig',
    'sphinx.ext.inheritance_diagram',
    'numpyext.only_directives',
    'numpyext.numpydoc',
    'numpyext.plot_directive',
    ]

todo_include_todos=True


#to have the docstring of the class and its init method
autoclass_content = 'both'


# Add any paths that contain templates here, relative to this directory.
templates_path = [ os.path.join(openalea ,'_templates')]

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'contents'

# General information about the project.
project = u'to be filled in a metainfo.ini at the same level as the setup.py'
copyright = None # to be dedined by the user
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
authors = None # to be define by the user
# The short X.Y version.
version = '1'
# The full version, including alpha/beta/rc tags.
release = '1'
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['_build']

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = 'TEST'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = os.path.join(openalea, 'images', 'wiki_logo_openalea.png')


# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = os.path.join(openalea, 'images', 'oaicon.ico')

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', os.path.join(openalea, '_static')]
html_style = 'openalea.css'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
html_index = 'index.html'

#Custom sidebar templates, maps page names to templates.
html_sidebars = {'index': 'indexsidebar.html'}
html_additional_pages = {   'index': 'index.html',
                            'openalea': 'openalea.html', 
                            'vplants': 'vplants.html',
                            'alinea': 'alinea.html'}

html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True
#html_copy_source = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
#htmlhelp_basename = 'to be done'


# -- Options for LaTeX output --------------------------------------------------

# NOT in original quickstart
pngmath_use_preview = True

# The paper size ('letter' or 'a4').
latex_paper_size = 'a4'

# The font size ('10pt', '11pt' or '12pt').
latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'main.tex', u'Documentation',
   u'username from metainfo.ini', 'manual'),
]

latex_elements = { 'inputenc': '\\usepackage[utf8x]{inputenc}' }

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = 

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
latex_preamble = """
   \usepackage{amsmath}
   \usepackage{amsfonts}
   \usepackage{amssymb}
   \usepackage{txfonts}"""

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None, 
                       'http://openalea.gforge.inria.fr/doc/openalea/core/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/deploy/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/deploygui/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/misc/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/scheduler/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/visualea/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/sconsx/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/openalea/stdlib/doc/_build/html': None,
                       'http://openalea.gforge.inria.fr/doc/vplants/stat_tool/doc/_build/html': None,


                    }
