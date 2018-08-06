#!/usr/bin/python

# This feature is experimental, and depends on ANSI truecolor, which not all
# terminals support.
class Color:
    def __init__(self, name, rgb, foreground=True):
        self.name = name
        self.rgb = rgb
        if foreground:
            self.prefix = "38"
        else:
            self.prefix = "48"

    def convertToNameAndEscape(self):
        output = [self.prefix, "2"]
        output.extend([str(x) for x in self.rgb])
        return self.name, ";".join(output)

################################################################################
# Add the RGB value for custom colors below; add False in the color constructor
# for background colors.
################################################################################
user_colors = [
#    Color("SkyBlue", (40,177,249))
]
