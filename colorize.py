#!/usr/bin/python

from sys import argv, stdin, stderr
from docopt import docopt
from collections import defaultdict
import re
import codecs

from signal import signal, SIGPIPE, SIG_DFL

colorListing = map(lambda x: (x[0].strip(), x[1].strip()), [
("Black            " , "30"),
("Red              " , "31"),
("Green            " , "32"),
("Yellow           " , "33"),
("Blue             " , "34"),
("Magenta          " , "35"),
("Cyan             " , "36"),
("White            " , "37"),
("Bright Black     " , "90"),
("Bright Red       " , "91"),
("Bright Green     " , "92"),
("Bright Yellow    " , "93"),
("Bright Blue      " , "94"),
("Bright Magenta   " , "95"),
("Bright Cyan      " , "96"),
("Bright White     " , "97"),
("BG_Black         " , "40"),
("BG_Red           " , "41"),
("BG_Green         " , "42"),
("BG_Yellow        " , "43"),
("BG_Blue          " , "44"),
("BG_Magenta       " , "45"),
("BG_Cyan          " , "46"),
("BG_White         " , "47"),
("BG_Bright Black  " , "100"),
("BG_Bright Red    " , "101"),
("BG_Bright Green  " , "102"),
("BG_Bright Yellow " , "103"),
("BG_Bright Blue   " , "104"),
("BG_Bright Magenta" , "105"),
("BG_Bright Cyan   " , "106"),
("BG_Bright White  " , "107"),
])
colorMap = {x[0].strip() : x[1] for x in colorListing}
colorPrefix = '\033['
colorSuffix = 'm'
colorReset = colorPrefix + '0' + colorSuffix

def addColor(line, colorNames):
  colorSequence = None
  if '|' not in colorNames:
    colorSequence = colorPrefix + colorMap[colorNames] + colorSuffix
  else:
    colorSequence = colorPrefix + ';'.join(colorMap[x] for x in colorNames.split("|")) + colorSuffix
  return "%s%s%s" % (colorSequence, line, colorReset)

def colorLine(line, patternMap, regexMap):
  for pattern in patternMap:
      if pattern in line:
          line = addColor(line, patternMap[pattern])
  for regex in regexMap:
      if regex.search(line):
          line = addColor(line, regexMap[regex])
          # No break, so last match wins.
  return line

# Only color the parts that match the pattern or regex.
def colorMatch(line, patternMap, regexMap):
  for pattern in patternMap:
      if pattern in line:
          parts = line.split(pattern)
          colored = addColor(pattern, patternMap[pattern])
          line = colored.join(parts)

  for regex in regexMap:
     parts = []
     m = regex.search(line)
     startIndex = 0
     while m:
       parts.append(line[startIndex:m.start()])
       parts.append(addColor(line[m.start():m.end()], regexMap[regex]))
       startIndex = m.end()
       m = regex.search(line[startIndex:])
     parts.append(line[startIndex:])
     line = ''.join(parts)
  return line


def removeInvalidMappings(patternMap):
    for x,y in patternMap.items():
      if ('|' not in y and y not in colorMap) or ('|' in y and any(c not in colorMap for c in y.split("|"))):
            print >> stderr, addColor("WARNING: Removing mapping '%s' --> '%s' due to unknown color '%s'." % (x,y,y), "Bright Red")
            del patternMap[x]

doc = r"""
Usage: ./colorize.py [-h] [-l] [-n] [-p <pattern>]... [-m <regex>]... [<input> ...]

    -h,--help                  show this
    -l,--listcolors            show the list of possible colors
    -p,--pattern <pattern>     specify the pattern in "pattern=color" form.
    -m,--match <regex>         specify the regex in "regex=color" form.
    -n,--onlymatch             when set, only the matching part of the line is colorized.
"""
def main():
    # Handle broken pipes when piping the output of this process to other
    # processes.
    signal(SIGPIPE,SIG_DFL)
    options = docopt(doc)
    if options['--listcolors']:
        print '\n'.join(addColor(x[0], x[0]) for x in colorListing)
        return
    patternMap = {y[0].strip(): y[1].strip() for y in (x.rsplit('=',1) for x in options['--pattern'])}
    regexMap = {re.compile("%s" % y[0].strip()): y[1].strip() for y in (x.rsplit('=',1) for x in options['--match'])}
    removeInvalidMappings(patternMap)
    removeInvalidMappings(regexMap)

    def colorize(f):
      for line in f:
        line = line.rstrip()
        if not options['--onlymatch']:
            line = colorLine(line, patternMap, regexMap)
        else:
            line = colorMatch(line, patternMap, regexMap)
        print line

    if len(options["<input>"]) == 0:
      colorize(stdin)
    else:
      for name in options["<input>"]:
        with open(name) as f:
          colorize(f)


if __name__ == '__main__':
    main()

