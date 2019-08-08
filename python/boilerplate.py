#!/usr/bin/env python3

"""
Basic boilerplate python script

This is a basic boilerplate python script intended to aid in writing a command line application.  I
am not a python programmer so this may not do everything correctly or the python way.

Features:
 - basic argument parsing
 - basic logging configuration
 - read files from both command line arguments and a file of files (-f)
 - transparently open gzip compressed files
 - argument parser for splitting a comma separated list into a python array
"""

import argparse
import io
import logging
import gzip
from os import path

# Program Version
__version__ = "0.1"

_LOGGER = logging.getLogger(path.basename(__file__))


class StoreList(argparse.Action):
    """Implementation of argparse.Action to store CSV into a python list"""
    #pylint: disable=R0903

    def __call__(self, parser, args, values, option_string=None):
        """Split value string from command line on comma and store it"""
        setattr(args, self.dest, values.split(','))

def handle_args():
    """
    Defines and processes command line arguments

    Returns:
        argparse.Namespace: processed arguments
    """
    parser = argparse.ArgumentParser(description="Boilerplate python script", \
        prog=path.basename(__file__))

    # Defaults for command line options
    parser.set_defaults(verbosity=0)

    # Example command line options.
    parser.add_argument("-v", "--verbose", action="count", dest="verbosity", \
        help="increase output (can be specified multiple times)")
    parser.add_argument("-f", "--file", type=argparse.FileType('r'), dest="filelist", \
        metavar="FILE", help="list of input files, one per line")
    parser.add_argument("-l", "--list", action=StoreList, dest="list", metavar="ITEM,...", \
        help="comma separated list of values")
    parser.add_argument('--version', action='version', \
        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument("files", type=argparse.FileType('rb'), nargs='*', metavar="FILE", \
        help="input file(s) to process.  Use '-' for stdin")

    args = parser.parse_args()

    # Process filelist, opening every file and adding file handle args.files.  We also expand
    # tilde (~) to the user's home directory in file paths
    if args.filelist is not None:
        if args.files is None:
            args.files = []
        for line in args.filelist:
            handle = open(path.expanduser(line.strip()), 'rb')
            args.files.append(handle)
        args.filelist.close()
        args.filelist = args.filelist.name

    # Check to see if any input files are gzip compressed and wrap the input stream to decompress
    # them on the fly
    if args.files is not None:
        for index in range(len(args.files)):
            if args.files[index].name.endswith(".gz"):
                args.files[index] = gzip.open(args.files[index])

    return args

def print_args(args):
    """
    Print parsed arguments

    This is a demo function to help you understand how command line arguments are being handled
    and should be removed when you write your program

    Args:
        args (): The program's argument list generated by argparser
    """
    print("verbosity: %d" % args.verbosity)
    if args.filelist is not None:
        print("file:  %s" % args.filelist)
    if args.list is not None:
        print("list:  [%s]" % " ".join(args.list))
    if args.files is not None:
        print("files [%s]" % " ".join([handle.name for handle in args.files]))

def read_files(files):
    """
    Read all lines of input files

    Note that argparse is configured to open all files in binary mode.  This is the most flexable
    and allows us to wrap file streams with a gzip decompressor if necessary.  Since this demo is
    for text files, we wrap the file streams with io.TextIOWrapper

    files: (): Array of file handles
    """
    for handle in files:
        for line in io.TextIOWrapper(handle):
            print("%s: '%s'" % (handle.name, line.strip()))

def main():
    """Main Function"""
    args = handle_args()

    if args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)

    ########################################################################
    # put your code here

    _LOGGER.warning("warning message")
    _LOGGER.info("info message")
    _LOGGER.debug("debug message")

    print_args(args)
    read_files(args.files)

    # Close open file handles.  Realistically, it is better to close these when finished with them
    for handle in args.files:
        handle.close()

    #
    ########################################################################

if __name__ == "__main__":
    main()