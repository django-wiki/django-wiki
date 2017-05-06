#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import argparse
import os
import signal
import subprocess
import sys


class RuntestsArgumentParser(argparse.ArgumentParser):
    def print_help(self):
        super(RuntestsArgumentParser, self).print_help()
        print("\n")
        print("All other arguments will be passed to pytest, \n"
              "which has the following options:\n")
        subprocess.call(["pytest", "--help"])

parser = RuntestsArgumentParser(usage="./runtests.py [args] [tests to run]\n\n"
                                "Individual tests can be run using pytest syntax e.g.\n\n"
                                "  ./runtests.py ./tests/core/test_views.py::ArticleViewViewTests::test_article_list_update\n")
parser.add_argument("--include-selenium", action='store_true',
                    help="Include Selenium tests, which are skipped by default. Requires chromedriver")
parser.add_argument("--show-browser", action='store_true',
                    help="Show browser window when running Selenium tests")


def main():
    known_args, remaining_args = parser.parse_known_args()
    cmd = ["pytest"] + remaining_args
    if known_args.include_selenium:
        # It is easier to use environment variables than to use 'pytest -k',
        # because the user might want to use that option.
        os.environ['INCLUDE_SELENIUM_TESTS'] = "1"
    if known_args.show_browser:
        os.environ['SELENIUM_SHOW_BROWSER'] = "1"

    # Signal handling to ensure the right thing happens
    # when Ctrl-C is pressed.
    SIGINT_RECEIVED = False

    def signal_handler(sig, f):
        global SIGINT_RECEIVED
        SIGINT_RECEIVED = True
        # No other action, just allow child to exit.


    signal.signal(signal.SIGINT, signal_handler)

    retcode = subprocess.call(cmd)

    if SIGINT_RECEIVED:
        sys.exit(1)
    else:
        sys.exit(retcode)

if __name__ == '__main__':
    main()
