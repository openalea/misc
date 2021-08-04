"""Tools related to sphinx."""
__license__ = "Cecill-C"

import os
import sys


def _upload_sphinx(package, force=False):
    """Upload the relevant html documentation to the wiki.

    Should be replace by an option in the setuptools.

    """

    if (os.path.isdir('../../' + package) and
        os.path.isdir('../doc') and
        os.path.isdir('./html/') and
        os.path.isdir('./latex/') and
        os.path.isfile('./latex/' + package + '.pdf')):

        print('Warning: these commands will be run. Is this what you want ? ')
        cmd1 = 'scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/sphinx/%s' % ('html', package.lower())
        print(cmd1)
        cmd2 = 'scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/sphinx/%s' % ('latex', package.lower())
        print(cmd2)

        if force:
            answer = 'y'
        else:
            answer = input('y/n ?')

        if answer == 'y':
            Tools.run(cmd1, test=False)
            Tools.run(cmd2, test=False)
    else:
        print('ERROR: You must be in the doc/ directory of the package.')
        print(' Maybe the html/ or latex/ directory does not exists')
        print(' or the latex/ directory does not contain a pdf file')
        sys.exit()
    # check that we are in ./opt.pacakge/doc and that there exists a latex and
    # html directory.


def sphinx_check_version():
    """Check that the sphinx version installed is greater than 0.6"""
    import sphinx
    if float(sphinx.__version__[0:3]) < 0.6:
        print(red('Sphinx 0.6 or higher required. found %s' % sphinx.__version__[0:3]))

        sys.exit(0)

