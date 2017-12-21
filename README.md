# font_generator
Script written in Python to convert images/svgs to font.

## How to use

Install [Fontforge](http://fontforge.github.io/en-US/downloads/)

##### run in MacOS
`/Applications/FontForge.app/Contents/MacOS/FontForge -quiet -script font_generator.py --output myfont.ttf --files *.svg --code 61440`

##### run in Linux
`fontforge -quiet -script font_generator.py --output myfont.ttf --files *.svg --code 61440`

## Options
| Option                           | Required     | Default         | Description                                            |
|:---:                             |:---:         |:---:            |:---                                                    |
| <pre>--output, -o</pre>          | *            |                 | The output font file.                                  |
| <pre>--files, -f</pre>           |              | []              | Images/Vectors to add in font.                         |
| <pre>--code, -c</pre>            |              | 61440           | The unicode of the images, if you pass more than one image, the anothers receive next codes. Accepts between 0-65535 |
| <pre>--map-name</pre>            |              |                 | The name of the glyphmap file.                         |
| <pre>--map-format</pre>          |              | json            | The type of the glyphmap file. (Accepts: json, ts-enum)|