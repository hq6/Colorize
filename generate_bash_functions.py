#!/usr/bin/env python

from colorize import colorMap

def main():
    colorPrefix = '\\033['
    colorSuffix = 'm'
    colorReset = colorPrefix + '0' + colorSuffix

    colorMacroNames = [color.upper().replace(" ", "_") + "()" for color in colorMap]
    print colorMacroNames
    nameMaxLength = max(len(x) for x in colorMacroNames)

    colorMacroDefinitions = [colorPrefix + colorMap[color] + \
            colorSuffix for color in colorMap]

    for n, d in zip(colorMacroNames, colorMacroDefinitions):
        output = '%-*s ' % (nameMaxLength, n)
        output += '{ echo -n -e "%s$@%s"; }' % (d, colorReset)
        print output


if __name__ == '__main__':
    main()
