"""Script to automatically generate sphinx documentation of an 
openalea package.

 
Example:

>>> python sphinx_tools --package core
>>>    --verbose  --project openalea   --inheritance

           
"""
__author__ = "$Author: Thomas.Cokelaer@sophia.inria.fr $"
__revision__ = "$Id: sphinx_tools.py 1695 2009-03-11 17:54:15Z cokelaer $"
__license__ = "Cecill-C"

import os
import sys
from optparse import OptionParser
import time
import warnings
try:
    from path import path
except ImportError:
    from openalea.core.path import path

# Some template to include in the reST files.


inheritance_string = '- Inheritance diagram:'

template_index = \
""".. _%(package)s_%(ref)s:

%(title)s

:Version: |version|
:Release: |release|
:Date: |today|

This manual details functions, modules, and objects included in 
%(Project)s.%(Package)s, describing what they are and what they do. For learning
how to use %(Project)s.%(Package)s see :ref:`%(package)s_%(link)s`.

.. warning::

   This Guide is still very much in progress.
   Many aspects of %(Project)s.%(Package)s are not covered.

   More documentation can be found on the
   `openalea <http://openalea.gforge.inria.fr>`__ wiki.

.. toctree::
    :maxdepth: 1
            
"""

template_source = \
"""
%(underline)s

.. htmlonly::

        :Revision: %(revision)s
        :License: %(license)s

        .. literalinclude:: %(source)s
            :linenos:
            :language: python
    
.. latexonly::

    .. note:: The source code is available from the SVN archive or the HTML version only.


"""

template_reference = \
""".. module:: %(module)s
    :synopsis: %(synopsis)s
            
%(title)s

:Revision: %(revision)s
:License: %(license)s

.. note:: The source file is available here below
    
.. toctree::
    :maxdepth: 0
       
    %(import_name_underscored)s_src.rst


Reference
********* 

%(inheritance_diagram)s

.. automodule:: %(import_name)s
    :members:
    :undoc-members:%(inheritance)s
    :show-inheritance:
    :synopsis: %(synopsis)s     
"""

template_contents = \
""".. _%(package)s:

.. module:: %(package)s

%(title)s

Module description
==================

.. sidebar:: Summary

    :Version: |version|
    :Release: |release|
    :Date: |today|
    :Author: See `Authors`_ section
    :ChangeLog: See `ChangeLog`_ section

.. topic:: Overview

    .. include:: user/overview.txt

Documentation
=============

.. toctree::
    :maxdepth: 1

    User Guide<user/index.rst>   
    Reference Guide<%(package)s/index.rst>

- A `PDF <../latex/%(package)s.pdf>`_ version of |%(package)s| documentation is 
  available.

.. seealso::

   More documentation can be found on the
   `openalea <http://openalea.gforge.inria.fr>`__ wiki.

Authors
=======

.. include:: ../AUTHORS.txt

ChangeLog
=========

.. include:: ../ChangeLog.txt

License
=======

|%(package)s| is released under a Cecill-C License.

.. note:: `Cecill-C <http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html>`_ 
    license is a LGPL compatible license.

.. |%(package)s| replace:: %(Project)s.%(Package)s
"""                                                         




configuration_templates = \
"""
# This import will 
#   - import sphinx ini in this directory
#   - import the common.ini in openalea/doc
#   - execute the statements in openalea/doc/common_conf.py
# you may overwrite some paramters found in common.ini here below

import sys
import os

sys.path.append(os.path.join(os.getcwd(), '../../../openalea/doc'))

from common_conf import *

# Overwrite extension if required
#extensions = [
#    'sphinx.ext.autodoc',
#    'sphinx.ext.doctest', 
#    'sphinx.ext.intersphinx',
#    'inheritance_diagram', 
#    'sphinx.ext.pngmath',
#    'sphinx.ext.todo', 
#    'numpydoc',
#    'phantom_import', 
#    'autosummary',
#    'sphinx.ext.coverage',
#    'only_directives'
#    ]


# to speed up compilation in development mode, uncomment this line
#intersphinx_mapping = {}
"""                                    










class SphinxToolsError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg + "$Name: $,  $Id: sphinx_tools.py 1695 2009-03-11 17:54:15Z cokelaer $"
    
    
class Tools(object):
    """to be done
    
    """
    def __init__(self):
        """
        """
        pass
    
    @staticmethod
    def add_time(foutput):
        """ function to add time at which the file was generated 

        :param foutput: a stream file, already opened
        """
        
        foutput.write(""".. Do not edit. 
.. File automatically generated by %s, revision %s, on %s\n\n""" % \
           ('sphinx_tools.py', __revision__.split(' ')[2], time.ctime()))
    
    @staticmethod
    def underline(text, symbol='^'):
        """
        print the text and an underline with the input symbol
    
        :param text: the text to print and underline
        :param symbol: symbol use to create the underline
        """
        _underline = text + '\n'
        _underline += symbol * len(text)
        return _underline

    @staticmethod
    def contains(this_file, words):
        """check the existence of keywords such as class and def in a file
    
        :param this_file: a filename
        :param words: words to find in the file
        """
        text = open(this_file,'r').read()
        lines = text.split('\n')
     
        for line in lines:
            for word in words:
                if word+' ' in line:
                    # remove all spaces. The class keyword should then be first,
                    # otherwise, it is either commented or a different 
                    # keyword (e.g., metaclass)
                    #line = line.replace(' ','')
                    if line.startswith(word):
                        return True
        return False
    
    @staticmethod            
    def run(cmd, verbose=True, test=True):
        """Simple run command alias

        :param verbose: set the verbose option to True (default) or False.
        :param test: set the test option to True (default) or False.

        If verbose is True, we print the command on the screen.
        If test if True then the command is not run.

        So, setting verbose and test arguments to True  allows to see the commands
        that will be run without launching them.
        """
        if verbose:
            print cmd
            if not test:
                os.system(cmd)


class PostProcess():
    """Provides functionalities to postprocess reST files generated with 
    sphinx_tools
        
    :param source: the filename of the source file
    :param verbose: a verbose option    
    """
    def __init__(self, source, verbose=True):
        self.source = source        
        self.text = open(self.source).read()
        self.backup_text = open(self.source).read()
        self.verbose = verbose
        
    def no_namespace_in_automodule(self):
        """remove the namespace provided in the automodule name
        
        useful when a package does not have yet a namespace
        """
        text = self.text
        if self.verbose:
            print '...remove namespace in automodule' + self.source
        try:
            if text.find('.. automodule::')==-1:
                if self.verbose:
                    print '...skip %s which do not contains any automodule directive' % self.source                
            else:
                lines = text.split('\n')
                foutput = open(self.source, 'w')
                for line in lines:
                    if '.. module::' not in line:
                        if '.. automodule::' in line:
                            line = line.replace('openalea.','')
                    foutput.write(line+'\n')
 
                foutput.close()
                self.update()
        except Exception, e:
            print e
            self.backup()
    
    def remove_header(self, nline, start=1):
        """remove the first nline lines of a file
        
        :param nline: number of lines to delete
        :param start: starting line (default is 1)
        """
        text = self.text
        if self.verbose:
            print '...remove header from '+self.source
        try:
            if text.find('.. module::')==-1:
                if self.verbose:
                    print '...skip %s which do not contains any module directive' % \
                        self.source                
            else:
                lines = text.split('\n')
                foutput = open(self.source, 'w')
                count = 1             
                for line in lines:
                    if count < start or count>= start + nline + 1:                    
                        foutput.write(line + '\n')
                    count += 1
                foutput.close()
                self.update()
        except Exception, e:
            print e
            self.backup()
        
    def switch_automodule_to_autofunction(self, function_list=None):
        """switch the name automodule to autofunction
        
        useful when a module contains only functions.
        :param function_list: list of function to comment (string)
        """
        if function_list == None:
            raise SphinxToolsError("""
You must provide the name of the function to document in the method 
switch_automodule_to_aufunction""")

        function_list = function_list.split(',')
        text = self.text        
        if self.verbose:
            print '...switching automodule to autofunction in ' + self.source
        if text.find('.. automodule::')!=-1:
            try:
                foutput = open(self.source,'w')
                foutput.write(text.split(".. automodule::")[0])
                text = text.split(".. automodule::")[1]
                
                for function in function_list:
                    foutput.write('.. autofunction:: ' + text.split('\n')[0]
                              + '.' + function)
                    foutput.write('\n')
                foutput.close()
                self.update()
            except:
                self.backup(text)
        else:
            print 'Seems to be done already.'
    

    def remove_inheritance(self):
        """function to remove inheritance-diagram section in a file"""
        # read the file once for all 
        try:
            if self.verbose:
                print '...remove inheritance from ' +self.source
            # open it to write the new file
            output = open(self.source,'w')
            # write the first part of the text before 'inheritance' bullet
            text = self.text.split(inheritance_string)
            output.write(text[0])
            # then, skip the inheritance-diagram directive
            for line in text[1].split('\n'):
                if ':parts: 2' in line or 'inheritance-diagram' in line:
                    continue
                else:
                    output.write(line +'\n')
            output.close()
            self.update()
        except:            
            self.backup()
            
    def remove_file(self):
        if self.verbose:
            print '...remove file ' +self.source
        os.remove(self.source)
            
    def backup(self):
        """if a problem occured, save the backup text in the original file"""
        output = open(self.source,'w')        
        output.write(self.backup_text)
        output.close()

    def update(self):
        self.text = open(self.source).read()
        
    def check_files(self):
        """check that a file exist
        """
        if os.path.isfile(self.source):
            pass
        else:
            raise SphinxToolsError("file %s was not found")
            


class Globber():
    """ This is a simple class to get the list of python 
    files contained in a directory and its sub-directories.
    
    It excludes the __init__ and __wralea__ files.
    
    The :func:`exclude_files` function allows to exclude more files, 
    
    The :func:`exclude_non_code` function excludes files that contains 
    no functions
    """
    
    def __init__(self, package=None, path=None, verbose=True):        
        self.path = path
        self.package = package 
        self.verbose = verbose
        self.files = []
        
    def __len__(self):
        return len(self.files)
                 
    def getfiles(self):
        """return list of python files to be scanned

        .. note:: do not include __init__ and __wralea__ file
        """ 
        from openalea.core.path import path

        if self.verbose:
            print 'Globbing files in package %s.' % self.package
            print 'in directory %s' % self.path    
            
        _directory = path(self.path)
        self.files = _directory.walkfiles('*.py')

        # convert self.files to a list of filenames 
        _list = []
        for this_file in self.files:
            _list.append(str(this_file))
            
        self.files = _list

        # exclude some files
        self.exclude_files('__wralea__.py')
        self.exclude_files('__init__.py')
        
        if self.verbose:
            self.print_len()
        return self.files
    
    def exclude_files(self, pattern):
        """Remove files that match the pattern

        .. note:: Changes self.files

        :param pattern: pattern to match 
        """
        # make a copy to loop over the original list
        _copy = self.files[:]
        
        for this_file in _copy:
            if pattern in this_file:
                self.files.remove(this_file)
        if self.verbose:
            self.print_len(pattern=pattern)
        
    def print_len(self, pattern=None):
        """alias to print the number of files"""
        if self.verbose:
            if pattern:
                print '...Remains %i files after exclusion of the pattern \'%s\'' \
                    % (self.__len__(), pattern)
            else:
                print '...Found %i files to parse' % self.__len__()

    def exclude_non_code(self):
        """do not consider files that contain neither classes nor 
        definitions

        .. note :: changes self.file 
        """
        _copy = self.files[:]
        for this_file in _copy:            
            if not Tools.contains(this_file, ['class', 'def']):
                self.files.remove(this_file)
                if self.verbose:
                    print 'Removed %s (no class,function found)' % this_file
                
        self.print_len()

        
class reST():
    """A class to generate reST code (API reference).
    
    .. todo:: __init__ to be cleaned
    """
    
    def __init__(self, 
                 fullname, package=None, project=None,
                 inheritance=None, opts=None):
        """
        .. todo:: to clean
        """
        self.fullname = fullname
        self.package = package
        self.project = project
        self.inheritance = inheritance
        self.opts = opts
        
        self.filename = os.path.split(self.fullname)[1]
        self.module = self.filename.split('.')[0]
        self.text_reference = ""
        self.text_source = ""
        self.path = path('..')/'doc'/self.package
        #self.path =  os.path.join('../doc',  self.package) 
        self.title = self.project + '.' + self.package + '.' + self.module
        self.import_name = 'to be done in next call'
        self.get_path_to_module(delimiter=self.project)
    
    def get_source(self):
        """.. todo:: make it robust"""
        
        try:            
            _name = self.fullname.split(os.path.join(self.package , 'src'))[1]
            if _name.startswith(os.sep):
                _name = _name.replace(os.sep, '', 1)             
            return path('..')/'..'/'src'/ _name
        except:
            
                    
            _name = path('..')/'..'/self.filename
            warnings.warn("source files should be in a src directory.")
            return _name

    def get_path_to_module(self, delimiter='openalea'):
        """Create the import name """
        
        openalea_packages = ['core', 'stdlib', 'deploy', 'deploygui', 
                             'misc', 'visualea', 'sconsx', 'PlantGL',
                             'fractalysis','stat_tool', 'newmtg',
                            'sequence_analysis','adel', 'caribu']
        
        if self.opts.debug:
            print 'PACKAGE ::::::::::: ', self.package, self.fullname
        if self.package in openalea_packages:
            try:
                _module = self.fullname.split(self.package + os.sep+'src')[1]
            except:
                if self.opts.debug:
                    print 'WARNING: exception caught. '
                    print 'WARNING: full name is %s and package is %s' % (self.fullname, self.package)
                _module = self.fullname.split(self.package)[1]
        else:
            _module = self.fullname.split(self.package + os.sep + 'src')[1]    
                
        _module = _module.replace('.py','') # has to be at the beginning
        _module = _module.replace('openalea'+os.sep, '.')
        _module = _module.replace(os.sep, '.')
        _module = _module.replace('..', '.')
        
        if self.project == 'OpenAlea':
            self.import_name = 'openalea' + _module
        elif self.project == 'VPlants':
            if self.package in ['PlantGL', 'stat_tool', 
                                'fractalysis', 'sequence_analysis']:
                self.import_name = 'openalea' + _module
            elif self.package == 'newmtg':
                self.import_name = 'openalea'+_module
                if self.opts.debug:
                    print '_module', _module
                    print self.import_name
            else:
                self.import_name = 'openalea.vplants' + _module
        elif self.project=='Alinea':
            if self.package in ['adel', 'caribu']:
                self.import_name = 'openalea' + _module
                
        else:
            raise SphinxToolsError(
                    'package and module combinaison not implemented') 
                   
    def get_vars(self, var=None):
        """import a module in the local scope 
        
        if `var` is not empty, returns only the `var` value
        """
        _dirname = os.path.dirname(self.fullname)
        sys.path.append(_dirname)        
        _scope = {}
        try:                     
            exec("import " + self.module + " as _module") in _scope
        except:
            
            # no need to repeat this warning
            if var == None:  
                warnings.warn("Exec failed to import module %s. %s" \
                              % (self.module, "Try to import manually to see the errors"))
                print 'debug ', _dirname
                print 'debug ', self.module
                print 'debug ', self.import_name 
            return ""
        else:
            if var == None:
                return _scope
            else:            
                if _scope['_module'].__dict__.has_key(var):
                    return _scope['_module'].__dict__[var]
                else:
                    return ""
            
    def synopsis(self):
        """ returns the first line of the __doc__ string"""
        
        scope = self.get_vars()
        
        if '_module' in scope:
            if scope['_module'].__doc__ is None:
                warnings.warn("Docstring of Module %s is None! (%s)" \
                              % (self.module, self.fullname))
                _doc = ".. note:: docstring of this module not found. Empty?"
            else:
                # only a limited numbers of characters () are shown in the 
                # synopsis, so we select only characters
                
                _doc = scope['_module'].__doc__[0:63]   
                if self.opts.debug:
                    print _doc
                # keep only the first line
                _doc = _doc.split('\n')[0]
                #if too long, add dots                
                if len(_doc)==63:
                    _doc = _doc[0:61] + '...'
                if self.opts.debug:
                    print '###----', _doc
                
        else:
            _doc = "Import of this module failed."
        
        return _doc
                
    def _create_text_reference(self):
        """todo"""
        
        if self.inheritance:
            inheritance = "\n    :inherited-members:"
            if Tools.contains(self.fullname, ['class']):
                inheritance_diagram = \
"""
%s

.. inheritance-diagram:: %s
    :parts: 2
""" % (inheritance_string, self.import_name)                
            else:
                inheritance_diagram = ''
        else: 
            inheritance = '' 
            inheritance_diagram = ''
                
        _params = {
                "module": self.module, 
                "title": Tools.underline(self.import_name + " API", '#'),
                "import_name_underscored": self.import_name.replace('.','_'),
                "inheritance_diagram": inheritance_diagram,
                "import_name": self.import_name, 
                "inheritance":inheritance,
                "synopsis":self.synopsis(),
                "revision": self.get_vars(var='__revision__'),
                "license": self.get_vars(var='__license__')
                }
        self.text_reference = template_reference % _params

    def _create_text_source(self):
        """todo"""       
        _params = {
              "title": self.title, 
              "underline": Tools.underline("Source file", '#'),                  
              "fullpathname": self.fullname,
              "source": self.get_source(),
              "revision": self.get_vars(var='__revision__'),
              "license": self.get_vars(var='__license__')
              }

        self.text_source = template_source % _params

    def write_reference(self):
        """todo"""
        
        # fill the string with missing values  
        self._create_text_reference()
                
        # save the resulting string in a text
        _stem = self.import_name.replace('.', '_')                
        
        #_output = open(self.path + os.sep + _stem + '_ref.rst' , "w")
        p = path(self.path) / _stem+'_ref.rst'
        _output = p.open(mode='w')
        
        if self.opts.verbose:
            print  '...'+_stem + '_ref.rst'
        Tools.add_time(_output)
        _output.write(self.text_reference)
        _output.close()
        
    def write_source(self):
        """todo"""
        # fill the string with missing values
        self._create_text_source()
        
        # save the resulting string in a text
        _stem = self.import_name.replace('.', '_')
        _output = open(self.path + os.sep + _stem + '_src.rst' , "w")
        Tools.add_time(_output)
        _output.write(self.text_source)
        _output.close()
        

def upload_sphinx(package, force=False):
    """
    Upload the relevant html documentation to the wiki. 
    should be replace by an option in the setuptools.
    
    """
    
    
    if os.path.isdir('../../' + package) and \
        os.path.isdir('../doc') and \
        os.path.isdir('./html/') and \
        os.path.isdir('./latex/') and \
        os.path.isfile('./latex/' + package + '.pdf'):
            
        print 'Warning: these commands will be run. Is this what you want ? ' 
        cmd1 = 'scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/sphinx/%s' % ('html', package.lower())
        print cmd1                
        cmd2 = 'scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/sphinx/%s' % ('latex', package.lower())
        print cmd2
        
        
        if force:
            answer = 'y'
        else:
            answer = raw_input('y/n ?')
                
        if answer == 'y':
            Tools.run(cmd1, test=False)
            Tools.run(cmd2, test=False)
    else:        
        print 'ERROR: You must be in the doc/ directory of the package.'
        print ' Maybe the html/ or latex/ directory does not exists'
        print ' or the latex/ directory does not contain a pdf file'        
        sys.exit()
    # check that we are in ./opt.pacakge/doc and that there exists a latex and 
    # html directory.
    
def check_project_name(project):
    """Check that the project name is correct and returns the appropriate 
    capitalisation. Correct names are openalea, vplants, alinea
    
    :param project: the name of a project to be checked
    :returns : None if the project name is wrong or the capitalised project name
    """
    if project.lower() == 'openalea':
        project = 'OpenAlea'
    elif project.lower() == 'vplants':
         project = 'VPlants'
    elif project.lower() == 'alinea':
        project = 'Alinea'
    else:
        project = None
        
    return (project)
            
            
def ParseParameters(check=True):
    """This is the main parsing function to get user arguments

    Example:
    
    >>> python sphinx_tools.py --package core --verbose --inheritance
    """

    usage = """Usage: %prog [options]

    This script generates the epydoc API of a module, copy it into ./module_name/doc-release
    and scp the content on the gforge URL at
          scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/

    Example:
    
    >>> python sphinx_tools.py --project openalea --package core  --verbose
    >>> python sphinx_tools.py --help

    """
    parser = OptionParser(usage=usage, \
        version = "%prog SVN $Id: sphinx_tools.py 1695 2009-03-11 17:54:15Z cokelaer $ \n" \
      + "$Name:  $\n"  + __author__)

    parser.add_option("-m", "--package", metavar='PACKAGE',
        default=None, 
        type='string',
        help="name of the module. E.g., core, visualea, stdlib")

    parser.add_option("-v", "--verbose", 
        action="store_true", 
        default=False, 
        help="verbose option on")
    
    parser.add_option("-d", "--debug", 
        action="store_true", 
        default=False, 
        help="debug option on")
    
    parser.add_option("-i", "--inheritance", 
        action="store_true", 
        default=False, 
        help="set inhereted-members in the module autodocumentation")

    parser.add_option("-n", "--project",  metavar='PROJECT',
        default=None,
        help="the project in which is contained the package <openalea, vplants, alinea>")
    
    parser.add_option("-u", "--upload",  metavar='UPLOAD',
        action="store_true",
        default=False,
        help="upload the project to the gforge")
    
    parser.add_option("-I", "--index",  metavar='INDEX',
        action="store_true",
        default=False,
        help="generate the index files")
    
    parser.add_option("-o", "--contents",  metavar='CONTENT',
        action="store_true",
        default=False,
        help="generate the content file")
      
    parser.add_option("-c", "--configuration",  metavar='CONFIGURATION',
        action="store_true",
        default=False,
        help="generate the configuration file conf.py for sphinx")
    
    parser.add_option("-f", "--force-upload",  metavar='CONTENT',
        action="store_true",
        default=False,
        help="do not request interactive session when uploading documentation")
    
    try:
        (_opts, _args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        return
    
    if check:  
        if not _opts.package:
            parser.error("--package must be provided! type --help to get help")
        
        if not _opts.project:
            parser.error("--project must be provided! type --help to get help")
    
        _opts.project = check_project_name(_opts.project)
        
        project = check_project_name(_opts.project)
        if project:
            pass
        else:
            parser.error("--project must be in ['openalea', 'vplants', 'alinea']")
        
        
    if _opts.upload:
        return _opts, _args

    return _opts, _args


def main(opts):
    """Main function of sphinx_tools

    This function get the list of python files (using globber class), then it 
    creates the reST files (using the reST class) and finally creates the index 
    and contents reST files if required. 
    
    :param opts: a structure containing the user parameters (--help for full help)
        
    """

    print """OpnAlea.Sphinx_Tools starting .................................."""
    print """...Starting initialisation of the files required by Sphinx"""
    if opts.index:
        print '...Will override user/index.rst and %s/index.rst' % opts.package
    else:
        print '...Will not override user/index.rst and %s/index.rst' % opts.package
        
    if opts.contents:
        print '...Will override contents.rst'
    else:
        print '...Will not override contents.rst'
    
    if opts.configuration:
        print '...Will override conf.py'
    else:
        print '...Will not override conf.py'
    text = None
    while text!='y' and text!='n':
        text = raw_input('carry on ? (y/n)')
        if text=='n':
            print 'stopped'
            sys.exit()
        elif text=='y':
            print 'Continue'
        
    
    # set some metadata and check arguments
    output_dir = '../doc/' + opts.package
    path = os.path.abspath('../')

    (_, cwd) = os.path.split(os.getcwd())
    if cwd == 'doc':
        pass
    else:
        raise SphinxToolsError("you must be in the doc/ directory.")
        
    
    # create an instance of globber to get the relevant python files
    globber = Globber(path=path, package=opts.package, verbose=opts.verbose)    
    
    # extract the python files
    globber.getfiles()
    
    # exclude some extra files
    # __wralea__ and __init__ are automatically excluded
    globber.exclude_files('test')
    globber.exclude_files('/doc/')
    globber.exclude_files('/build/')
    globber.exclude_files('setup.py')

    # those files that do contains nor class neither functions
    globber.exclude_non_code()
      
    # sort the files
    globber.files.sort()
    

    # create the reST outputs
    
    for directory in ['user', output_dir, '.static']:
        try:        
            os.mkdir(directory)
        except:
            warnings.warn('Directory %s/ already exists. ' % directory)
    if os.path.isfile('user/overview.txt'):
        pass
    else:
        output = open('user/overview.txt', 'w')
        output.write('to be done')
        output.close()
        
    
    if opts.verbose:
        print 'Creating reST files and copying them into %s.' % output_dir
    
    # Create all the reST files for each module
    for module in globber.files:
        output = reST(module, 
                      package=opts.package, 
                      project=opts.project, 
                      inheritance=opts.inheritance,
                      opts=opts)
        output.write_reference()
        output.write_source()
            
    # create the index for the reference and user guides
    # the user guide first
    title = ' User Guide'
    params = {'title': Tools.underline(opts.package.capitalize() + title , '#'),
              'Package': opts.package.capitalize(),
              'Project': opts.project,
              'package': opts.package,
              'project': opts.project.lower(),                             
              'link':'reference',
              'ref':'user'
              }
    
    # specific to the user guide
    if opts.index:
        foutput_user = open(os.path.join(output_dir ,'../user/index.rst'), 'w')
        Tools.add_time(foutput_user)
        foutput_user.write(template_index % params)
        foutput_user.write("    *rst\n")    
        foutput_user.close()
    
    # specific to the reference guide
    # reset the title
    params['title'] = Tools.underline(opts.package.capitalize() + 
                                " Reference Guide", '#')
    # and change the link
    params['link'] = 'user'
    params['ref'] = 'reference'    


    if opts.index:
        foutput_ref = open(os.path.join(output_dir, 'index.rst'), 'w')
        Tools.add_time(foutput_ref)              
        foutput_ref.write(template_index % params)
        for item in globber.files:   
            data = reST(item,
                        opts.package, 
                        opts.project,opts=opts)
            foutput_ref.write('    ' + data.import_name.replace('.', '_') 
                              +  '_ref.rst\n')
        foutput_ref.close()
    
    # create the contents rst file
    if opts.contents:
        foutput = open(output_dir + '/../contents.rst','w')
        params['title'] = Tools.underline(
            opts.project + " " + opts.package.capitalize() 
            + " documentation", '#')
        Tools.add_time(foutput)
        foutput.write(template_contents % params)
        foutput.close()
        
    if opts.configuration:
        foutput = open(output_dir + '/../conf.py','w')
        foutput.write(configuration_templates)
        foutput.close()

    # finalise
    if opts.verbose:
        print """ 
    
    Running the postprocess.py python file within the 
    %s/doc directory to clean up some known issues within the
    reST files that have just been automatically generated
    """ % opts.package
    
    if os.path.isfile('postprocess.py'):
        Tools.run('python postprocess.py', verbose=True, test=False)
    else:
        if opts.verbose:
            print 'No postprocess.py file found. continue'
        
        
    print 'Done'
    print 'Normal Termination (use --verbose or --debug to get more info in case of trouble)'



if __name__ == '__main__':

    # get user parameters
    (_opts, _) = ParseParameters()
    if not _opts.verbose:
        warnings.simplefilter("ignore")
    # if upload is requested, nothing else to do
    if _opts.upload:
        upload_sphinx(package=_opts.package, force=_opts.force_upload)
        sys.exit()
        
    # otherwise, go to the main function
    main(_opts)

def init():
    """
    
    function linked to the script alea_init_sphinx. 
    
    Works like sphinx_tools.py module but it is possible to use it without 
    the --package and --project arguments, which will be read from the sphinx.ini
    file if present in the directory
    
    :Usage:
        From the ./doc directory type:
        
        alea_init_script --package core --project openalea --verbose
        alea_init_script --package core --project openalea 
        alea_init_script --verbose
        alea_init_script --index --contents
    
    """
    if os.path.basename(os.getcwd())=='doc':
        pass
    else:
        raise SphinxToolsError("must be in the doc directory of a package to use this program")
            
    (optss, _args) = ParseParameters(check=False)
    
    # providing the package name and project are optional. 
    if optss.project is None and optss.package is None:
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        config.read('sphinx.ini')       # same dir as the conf.py's location
        try:
            section = 'metadata'
            config.options(section)
        except:
            raise SphinxToolsError('sphinx.ini file needs to be present in the doc directory')
            
        if 'project' in config.options(section):
            project = config.get(section, 'project')
        if 'package' in config.options(section):
            package = config.get(section, 'package')
    
        optss.project = project
        optss.package = package
        
        
    optss.project = check_project_name(optss.project)
    if optss.project is None: 
        raise SphinxToolsError("sphinx.ini does not contain a valid project option")

    if optss.project:
        main(optss)
    else:
        raise SphinxToolsError("--project must be in ['openalea', 'vplants', 'alinea']")
   

