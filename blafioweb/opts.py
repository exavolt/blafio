#!/usr/bin/env python

from tornado.options import define as opt


opt("config", default=None, help=
    "Config file name to load")
opt("daemon", default=False, type=bool, help=
    "Run as daemon")

opt("host", default="", help=
    "Listen to the specified host")
opt("port", default=11001, type=int, help=
    "Run on the given port")

opt("db_name", default="blafio", help=
    "DB Name")
opt("db_host", default=None, help=
    "DB server address")
opt("db_port", default=None, type=int, help=
    "DB server port")
opt("db_usr", default=None, help=
    "DB username")
opt("db_pwd", default=None, help=
    "DB password")


if __name__ == "__main__":
    import sys
    from tornado.options import options
    ignored_options = ['help', 'config']
    outf = sys.stdout
    by_file = {}
    for option in options.itervalues():
        by_file.setdefault(option.file_name, []).append(option)
    print >> outf, """\
# All the rules for this config file are the same with the command line options.
# The options available could be found out by passing `--help` to the main.py
"""
    print >> outf, "#- buit-in options -\n"
    for filename, o in sorted(by_file.items()):
        if filename: print >> outf, "\n#- " + filename + " -\n"
        o.sort(key=lambda option: option.name)
        for option in o:
            if option.name in ignored_options:
                continue
            prefix = option.name
            suffix = ""
            if option.metavar:
                suffix = " # " + option.metavar
            if option.value() is None:
                print >> outf, "%s = None %s" % (prefix, suffix)
            elif option.type in [str, unicode]:
                #TODO: escape unicode
                print >> outf, "%s = \"%s\" %s" % (prefix, 
                    option.value() or "", suffix)
            elif option.type == bool:
                print >> outf, "%s = %s %s" % (prefix, 
                    "True" if option.value() else "False", suffix)
            else:
                print >> outf, "%s = %s %s" % (prefix, 
                    option.value() or "", suffix)
    print >> outf, "\n"
    

