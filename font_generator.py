# -*- coding: utf-8 -*-
import fontforge, os, argparse, re
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('UTF8')

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", required=True, help="set output font")
    parser.add_argument("--files", "-f", nargs='+', default=[], help="files to add in font")
    parser.add_argument("--code", "-c", type=int, default=61440, help="the code of the glyph, if you pass more than one, the anothers receive next codes")

    args = parser.parse_args()

    if args.output:
        outputFile = args.output
    listGlyphs = args.files
    code = args.code

    dict_glyphmaps = generateFont(outputFile, listGlyphs, code)
    generate_glyphmaps(dict_glyphmaps)
    exit(0)

def generateFont(outputFile, listGlyphs, codePoint):
    print 'glyph files: ' + str(len(listGlyphs))

    font = fontforge.font()
    font.fontname = os.path.splitext(os.path.basename(outputFile))[0]

    dict_glyphmaps = {}

    # add chars
    for fileName in listGlyphs:
        glyph = font.createChar(codePoint).importOutlines(fileName)

        if glyph.validate() == 0:
            print 'file with error: ' + fileName
            continue

        # align in left
        glyph.left_side_bearing = 0
        # set width
        x_max = glyph.boundingBox()[2]
        glyph.width = glyph.vwidth = x_max

        # add glyphmap
        basename = os.path.splitext(os.path.basename(fileName))[0]
        dict_glyphmaps[basename] = codePoint

        codePoint += 1

    font.generate(outputFile)
    print 'Generate font: ' + outputFile
    return dict_glyphmaps

def generate_glyphmaps(dict_glyphmaps):
    file = open("glyphmaps.ts", "w+")
    file.write('export default {\n')
    glyph_items = sorted(dict_glyphmaps.items(), key=itemgetter(1))
    for key, value in glyph_items:
        line_break = ',\n' if key != glyph_items[-1][0] else ''
        file.write('    "{0}": {1}{2}'.format(key, dict_glyphmaps[key], line_break))
    file.write('\n}')
    file.close()

if __name__ == "__main__":
    main(sys.argv)