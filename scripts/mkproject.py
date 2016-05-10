#!/usr/bin/python

"""
  python-dirtt - Directory Tree Templater
  (c) 2015 Robert Moggach and contributors
  Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

    mkproject.py

    This is a generic command line tool that prompts for template
    variables in a given template and renders the tree.

"""

import os
import sys
from optparse import OptionParser

from dirtt import DirectoryTreeHandler, list_available_templates
from dirtt.util.template import return_placeholders

ENABLED_USERS = [0,1111]
TEMPLATE_ROOT="/studio/tools/var/dirtt/templates"
TEMPLATE_ROOT="/Users/rob/Code/python-dirtt-templates"
TEMPLATE_DIR=os.path.join(TEMPLATE_ROOT,"project")
PROJECT_ROOT="/studio/jobs"
PROJECT_TEMPLATE=os.path.join(TEMPLATE_DIR,"project.xml")


def main():
    usage = "usage: %prog [-t TEMPLATE]"
    version=__import__('dirtt').get_version()
    description="""Interactively create a directory tree from template(s)."""
    parser = OptionParser(usage=usage, version=version, description=description)
    parser.add_option("-p", "--project", dest="project_path", action="store")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    parser.add_option("-i", "--interactive", dest="interactive", action="store_true", default=False)
    parser.add_option("-w", "--stop-on-warning",dest="warn",action="store_true",default=False)
    (options, args) = parser.parse_args()
    if os.geteuid() not in ENABLED_USERS:
        print "You are not authorized to run this script."
        sys.exit(-6)
    if options.verbose: verbose = True
    else: verbose = False
    if options.interactive: interactive = True
    else: interactive = False
    if options.warn:  warn = True
    else: warn = False

    template_variables = {}
    template_variables["project_root"] = PROJECT_ROOT


    if options.project_path:
        project_path = options.project_path
    else:
        project_path = None
        print "Enter the project_path:\n\tEg. hyundai/etne"
        project_path=raw_input("\tproject_path >  ")
    if not project_path:
        print "\n  You must specify a project_path Eg. hyundai/etne \n"
        sys.exit(-6)
    print "\n  Project ROOT: %s" % PROJECT_ROOT
    project_path_full=os.path.join(PROJECT_ROOT,project_path)
    print "\n  Project Path: %s" % project_path_full
    template_variables["project_path"] = project_path
    if not os.path.isdir(project_path_full):
        c = DirectoryTreeHandler(verbose,PROJECT_TEMPLATE,template_variables,interactive,warn)
        c.run()
        print "\n  Created Project Tree."
    else:
        print "\n  Project Path Exists."

    sys.exit(0)


if __name__ == "__main__":
    main()
