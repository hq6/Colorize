#!/usr/bin/env python

from __future__ import print_function
from sys import argv, stdin, stderr
from docopt import docopt
from collections import OrderedDict
import re
import codecs

from signal import signal, SIGPIPE, SIG_DFL

colors = [
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
]
colorListing = map(lambda x: (x[0].strip(), x[1].strip()), colors)
colorMap = OrderedDict((x[0].strip() , x[1]) for x in colorListing)

def addColor(line, colorNames):
  colorPrefix = '\033['
  colorSuffix = 'm'
  colorReset = colorPrefix + '0' + colorSuffix

  if colorNames == None:
    return line
  colorSequence = None
  if '|' not in colorNames:
    colorSequence = colorPrefix + colorMap[colorNames] + colorSuffix
  else:
    colorSequence = colorPrefix + ';'.join(colorMap[x] for x in colorNames.split("|")) + colorSuffix
  return "%s%s%s" % (colorSequence, line, colorReset)

def colorLine(line, fixedstringMap, regexMap):
  outLine = None
  for regex in regexMap:
      if regex.search(line):
          outLine = addColor(line, regexMap[regex])
          # No break, so last match wins.
  for fixedstring in fixedstringMap:
      if fixedstring in line:
          outLine = addColor(line, fixedstringMap[fixedstring])
  if outLine:
    return outLine
  return line

# Only color the parts that match the fixedstring or regex.
def colorMatch(line, fixedstringMap, regexMap):
  if len(line) == 0: return line
  # Determine the color for each character
  characterColors = [None] * len(line)

  for regex in regexMap:
     m = regex.search(line)
     startIndex = 0
     while m:
       characterColors[m.start() : m.end()] = [regexMap[regex]] * (m.end() - m.start())
       startIndex = m.end()
       m = regex.search(line, startIndex)

  for fixedstring in fixedstringMap:
      startIndex = line.find(fixedstring)
      while startIndex != -1:
        endIndex = startIndex + len(fixedstring)
        characterColors[startIndex : endIndex] = [fixedstringMap[fixedstring]] * (endIndex - startIndex)
        startIndex = line.find(fixedstring, endIndex)

  # Postprocess based on the color of each character
  outLine = ''
  curColor = characterColors[0]
  curIndex = 0
  for i, c in enumerate(characterColors):
      if c != curColor:
          outLine += addColor(line[curIndex:i], curColor)
          curColor = c
          curIndex = i
  outLine += addColor(line[curIndex:], curColor)
  return outLine


def isValidColor(color):
    return (color in colorMap) or ('|' in color and all(c in colorMap for c in color.split("|")))

def removeInvalidMappings(fixedstringMap):
    for x,y in fixedstringMap.items():
      if not isValidColor(y):
            print(addColor("WARNING: Removing mapping '%s' --> '%s' due to unknown color '%s'." % (x,y,y), "Bright Red"), file=sys.stderr)
            del fixedstringMap[x]

def createColoredLine(chars, color, length=80):
    out = ""
    for i in range(length):
        out += chars[i % len(chars)]
    return addColor(out, color)

doc = r"""
Usage: ./colorize.py [-h] [-l] [-g <color>] [-n] [-f <fixedstring>]... [-m <regex>]... [<input> ...]

    -h,--help                       show this
    -l,--listcolors                 show the list of possible colors
    -f,--fixedstring <fixedstring>  specify the fixedstring in "fixedstring=color" form.
    -m,--match <regex>              specify the regex in "regex=color" form.
    -n,--onlymatch                  when set, only the matching part of the line is colorized.
    -g,--generate <color>           generate a horizontal line of the specified color
"""
def main():
    # Handle broken pipes when piping the output of this process to other
    # processes.
    signal(SIGPIPE,SIG_DFL)
    options = docopt(doc)
    if options['--listcolors']:
        print('\n'.join(addColor(x[0], x[0]) for x in colorListing))
        return
    if options['--generate']:
        symbol = "="
        color = None
        if '=' in options['--generate']: symbol, color = options['--generate'].rsplit('=',1)
        else: color = options['--generate']
        if isValidColor(color):
            print(createColoredLine(symbol, color))
        else:
            print(addColor("ERROR: Invalid color '%s' specified!" % color, "Bright Red"))
        return

    try:
        fixedstringMap = OrderedDict((y[0].strip(), y[1].strip()) for y in (x.rsplit('=',1) for x in options['--fixedstring']))
        regexMap = OrderedDict((re.compile("%s" % y[0].strip()), y[1].strip()) for y in (x.rsplit('=',1) for x in options['--match']))
    except re.error as err:
        print("Error parsing regular expression:", err)
        return
    except:
        print("At least one of the fixed strings or regular expressions is missing an '=' sign.")
        return
    removeInvalidMappings(fixedstringMap)
    removeInvalidMappings(regexMap)

    def colorize(f):
      for line in f:
        line = line.rstrip()
        if not options['--onlymatch']:
            line = colorLine(line, fixedstringMap, regexMap)
        else:
            line = colorMatch(line, fixedstringMap, regexMap)
        print(line)

    if len(options["<input>"]) == 0:
      colorize(stdin)
    else:
      for name in options["<input>"]:
        with open(name) as f:
          colorize(f)


if __name__ == '__main__':
    main()

