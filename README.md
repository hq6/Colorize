# ColorizeLines.py

There is at least one [existing tool](http://pygments.org/) to perform
automatic syntax highlighting of code and output ANSI escape sequences.
Unfortunately, to the best of the author's knowledge, there is no existing
tool for highlighting lines of log files that contain a particular pattern.
Vim's `match` and `2match` are close, but a little kludgy to use.

The purpose of this tool is to colorize lines matching a particular pattern, to
make it easier to highlight relevant lines in a log file, when poring over such
files with your coworker or manager.

### Usage

    colorize.py -h
    colorize.py -l
    colorize.py -p 'This is an interesting line=Blue' Input.log
    colorize.py -p 'This is an interesting line=Blue' -p 'Different topic=Red' Input.log

    # Note that we run less in raw node
    colorize.py -p 'This is an interesting line=Blue' | less -R
