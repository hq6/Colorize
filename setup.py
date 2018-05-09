from setuptools import setup

long_description=\
"""
colorize.py
==================

There is at least one [existing tool](http://pygments.org/) to perform
automatic syntax highlighting of code and output ANSI escape sequences.
Unfortunately, to the best of the author's knowledge, there is no existing
tool for highlighting lines of log files that contain a particular pattern.
Vim's `match` and `2match` are close, but a little kludgy to use.

The purpose of this tool is to colorize lines matching a particular pattern, to
make it easier to highlight relevant lines in a log file, when poring over such
files with your coworker or manager.

Usage
==================


Assume we have a file with the following contents.::

    This is an interesting line with some awesome content.
    unrelated line
    unrelated line
    unrelated line
    foobar
    Different topic of interest
    unrelated line

Then we can run the following commands to see some of effects we want.::

    colorize.py -h
    colorize.py -l
    colorize.py -f 'This is an interesting line=Blue' Input.log
    colorize.py -f 'This is an interesting line=Blue' -f 'Different topic=Red' Input.log

    # Note that we must run less in raw node to see the colors.
    colorize.py -f 'This is an interesting line=Blue' | less -R
"""

setup(
  name="colorize.py",
  version='0.6',
  scripts=['colorize.py'],
  install_requires=['docopt>=0.2'],
  author="Henry Qin",
  author_email="root@hq6.me",
  description="Add colors to plain text lines matching either a Python string or regular expression",
  long_description=long_description,
  platforms=["Any Platform supporting ANSI escape codes"],
  license="MIT",
  url="https://github.com/hq6/Colorize"
)
