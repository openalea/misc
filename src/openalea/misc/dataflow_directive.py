"""A special directive for including a visualea dataflow.

usage
=====

::


    .. dataflow:: package_name node_name
        width: 50%

        your caption


options are identical to the image/plot/figure directives (width, scale, height, ...)

An additional caption may be added

Based on plot_directives from matplotlib.

author: Thomas Cokelaer
"""

from PyQt4 import QtGui
from openalea.core.alea import *
from openalea.visualea.dataflowview import GraphicalGraph
app = QtGui.QApplication([])

pm = PackageManager()
pm.init()
import matplotlib.cbook as cbook

import sys, os, shutil, imp, warnings, cStringIO, re
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from docutils.parsers.rst import directives
try:
    # docutils 0.4
    from docutils.parsers.rst.directives.images import align
except ImportError:
    # docutils 0.5
    from docutils.parsers.rst.directives.images import Image
    align = Image.align
import sphinx

sphinx_version = sphinx.__version__.split(".")
# The split is necessary for sphinx beta versions where the string is
# '6b1'
sphinx_version = tuple([int(re.split('[a-z]', x)[0])
                        for x in sphinx_version[:2]])

from matplotlib.sphinxext import only_directives


class DataflowWarning(Warning):
    """Warning category for all warnings generated by this directive.

    By printing our warnings with this category, it becomes possible to turn
    them into errors by using in your conf.py::

      warnings.simplefilter('error', plot_directive.DataflowWarning)

    This way, you can ensure that your docs only build if all your examples
    actually run successfully.
    """
    pass



template = """
.. htmlonly::

   %(links)s

   .. figure:: %(prefix)s%(tmpdir)s/%(outname)s.png
%(options)s

%(caption)s

.. latexonly::
   .. figure:: %(prefix)s%(tmpdir)s/%(outname)s.pdf
%(options)s

%(caption)s

"""

exception_template = """
.. htmlonly::

   [`source code <%(linkdir)s/%(basename)s.py>`__]

Exception occurred rendering plot.

"""

template_content_indent = '      '

def out_of_date(original, derived):
    """
    Returns True if derivative is out-of-date wrt original,
    both of which are full file paths.
    """
    return (not os.path.exists(derived) or
            (os.path.exists(original) and
             os.stat(derived).st_mtime < os.stat(original).st_mtime))

def run_code(plot_path, package_name, node_name, basename, tmpdir, destdir):
    """
    Import a Python module from a path, and run the function given by
    name, if package_name is not None.
    """
    pkg = pm[package_name]

    factory = pkg.get_factory(node_name)
    node = factory.instantiate()

    view = GraphicalGraph.create_view(node)
    view.show()

    outname = 'dataflow_' + node_name
    outpath = os.path.join(tmpdir, outname)

    filename = outpath 

    rect = view.scene().sceneRect()
    matrix = view.matrix()
    rect = matrix.mapRect(rect)

    pixmap = QtGui.QPixmap(rect.width(), rect.height())
    pixmap.fill()
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    view.update()
    #view.render(painter)
    view.scene().render(painter)
    painter.end()
    pixmap.save(filename+'.png', "png")
    #pixmap.save(filename+'.svg', "svg")
    #print '########################################################3'
    #image = pixmap.toImage()
    #image.save(filename+'.pdf', 'PDF')
    view.close()
    return 1



def render_figures(plot_path, package_name, node_name, tmpdir, destdir):
    """
    Run a pyplot script and save the low and high res PNGs and a PDF
    in outdir.
    """
    plot_path = str(plot_path)  # todo, why is unicode breaking this
    basedir, fname = os.path.split(plot_path)
    basename, ext = os.path.splitext(fname)
    #print  'DATAFLOW plot_path and basename', plot_path, basename
    all_exists = True

    # Look for single-figure output files first
    for format in ['png']:
        outname = os.path.join(tmpdir, '%s.%s' % (basename, format))
        if out_of_date(plot_path, outname):
            all_exists = False
            break

    if all_exists:
        return 1

    # Then look for multi-figure output files, assuming
    # if we have some we have all...
    i = 0
    while True:
        all_exists = True
        for format in ['png']:
            outname = os.path.join(
                tmpdir, '%s_%02d.%s' % (basename, i, format))
            if out_of_date(plot_path, outname):
                all_exists = False
                break
        if all_exists:
            i += 1
        else:
            break

    if i != 0:
        return i

    # We didn't find the files, so build them

    run_code(plot_path, package_name, node_name, basename, tmpdir, destdir)


    return 1

def _plot_directive(plot_path, basedir, package_name, node_name, caption,
                    options, state_machine):
    formats = ['png']

    fname = os.path.basename(plot_path)
    basename, ext = os.path.splitext(fname)

    # Get the directory of the rst file, and determine the relative
    # path from the resulting html file to the plot_directive links
    # (linkdir).  This relative path is used for html links *only*,
    # and not the embedded image.  That is given an absolute path to
    # the temporary directory, and then sphinx moves the file to
    # build/html/_images for us later.
    rstdir, rstfile = os.path.split(state_machine.document.attributes['source'])
    outdir = os.path.join('dataflow_directive', basedir)
    reldir = os.path.relpath(setup.confdir, rstdir)
    linkdir = os.path.join(reldir, outdir)

    # tmpdir is where we build all the output files.  This way the
    # plots won't have to be redone when generating latex after html.

    tmpdir = os.path.join('build', outdir)
    tmpdir = os.path.abspath(tmpdir)
    prefix = '/'
    if not os.path.exists(tmpdir):
        cbook.mkdirs(tmpdir)

    # destdir is the directory within the output to store files
    # that we'll be linking to -- not the embedded images.
    destdir = os.path.abspath(os.path.join(setup.app.builder.outdir, outdir))
    if not os.path.exists(destdir):
        cbook.mkdirs(destdir)

    # Properly indent the caption
    caption = '\n'.join(template_content_indent + line.strip()
                        for line in caption.split('\n'))

    # Generate the figures, and return the number of them
    num_figs = render_figures(plot_path, package_name, node_name, tmpdir, destdir)

    # Now start generating the lines of output
    lines = []

    if node_name is None:
        shutil.copyfile(plot_path, os.path.join(destdir, fname))


    if num_figs > 0:
        options = ['%s:%s: %s' % (template_content_indent, key, val)
                   for key, val in options.items()]
        options = "\n".join(options)

        outname = basename
        outname = 'dataflow_'+node_name
        links = []
        if node_name is None:
            links.append('`source code <%(linkdir)s/%(basename)s.py>`__')
        if len(links):
            links = '[%s]' % (', '.join(links) % locals())
        else:
            links = ''

        lines.extend((template % locals()).split('\n'))

    if len(lines):
        state_machine.insert_input(
            lines, state_machine.input_lines.source(0))

    return []

def plot_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):
    """
    Handle the arguments to the plot directive.  The real work happens
    in _plot_directive.
    """
    # The user may provide a filename *or* Python code content, but not both
    if len(arguments):

        plot_path = './build'
        #plot_path = ''
        basedir = os.path.relpath(os.path.dirname(plot_path), setup.app.builder.srcdir)
        # If there is content, it will be passed as a caption.

        # Indent to match expansion below.  XXX - The number of spaces matches
        # that of the 'options' expansion further down.  This should be moved
        # to common code to prevent them from diverging accidentally.
        caption = '\n'.join(content)

        # If the optional function name is provided, use it
        if len(arguments) == 2:
            package_name = arguments[0]
            node_name = arguments[1]
        else:
            raise ValueError("expect 2 arguments")
        print 'Dataflow extension: processing %s.%s ' % (package_name, node_name)
        try:

            return _plot_directive(plot_path, basedir, package_name, node_name, caption,
                               options, state_machine)
        except:
            DataflowWarning("dataflow sphinx extension failed while processing %s %s" % (package_name, node_name))

def mark_plot_labels(app, document):
    """
    To make plots referenceable, we need to move the reference from
    the "htmlonly" (or "latexonly") node to the actual figure node
    itself.
    """
    for name, explicit in document.nametypes.iteritems():
        if not explicit:
            continue
        labelid = document.nameids[name]
        if labelid is None:
            continue
        node = document.ids[labelid]
        if node.tagname in ('html_only', 'latex_only'):
            for n in node:
                if n.tagname == 'figure':
                    sectname = name
                    for c in n:
                        if c.tagname == 'caption':
                            sectname = c.astext()
                            break

                    node['ids'].remove(labelid)
                    node['names'].remove(name)
                    n['ids'].append(labelid)
                    n['names'].append(name)
                    document.settings.env.labels[name] = \
                        document.settings.env.docname, labelid, sectname
                    break

def setup(app):
    setup.app = app
    setup.config = app.config
    setup.confdir = app.confdir

    options = {'alt': directives.unchanged,
               'height': directives.length_or_unitless,
               'width': directives.length_or_percentage_or_unitless,
               'scale': directives.nonnegative_int,
               'align': align,
               'class': directives.class_option,
               'include-source': directives.flag,
               'encoding': directives.encoding }

    app.add_directive('dataflow', plot_directive, True, (0, 2, 0), **options)

    app.connect('doctree-read', mark_plot_labels)
