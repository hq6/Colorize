#!/usr/bin/env python

from colorize import colorMap

def main():
    colorPrefix = '"\\033['
    colorSuffix = 'm"'
    colorReset = colorPrefix + '0' + colorSuffix

    colorMacroNames = [color.upper().replace(" ", "_") + "(X)" for color in colorMap]
    nameMaxLength = max(len(x) for x in colorMacroNames)

    colorMacroDefinitions = [colorPrefix + colorMap[color] + \
            colorSuffix for color in colorMap]
    definitionMaxLength = min(max(len(x) for x in colorMacroDefinitions), 12)

    for n, d in zip(colorMacroNames, colorMacroDefinitions):
        output = 'function  %-*s ' % (nameMaxLength, n)
        output += '{ return %-*s X %s }' % (definitionMaxLength, d, colorReset)
        print output


if __name__ == '__main__':
    main()
