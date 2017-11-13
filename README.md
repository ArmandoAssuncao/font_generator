# font_generator
Script written in Python to convert images/svgs to font.

## How to use

Install [Fontforge](http://fontforge.github.io/en-US/downloads/)

##### run in MacOS
`/Applications/FontForge.app/Contents/MacOS/FontForge -quiet -script font_generator.py --output myfont.ttf --files *.svg --code 61440`

##### run in Linux
`fontforge -quiet -script font_generator.py --output myfont.ttf --files *.svg --code 61440`
