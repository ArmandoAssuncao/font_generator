# -*- coding: utf-8 -*-
import fontforge, os, argparse, re
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('UTF8')

map_formats = {
    "json": "json",
    "ts-enum": "ts-enum"
}

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", required=True, help="The output font file.")
    parser.add_argument("--files", "-f", nargs='+', default=[], help="Images/Vectors to add in font.")
    parser.add_argument("--code", "-c", type=int, default=61440, help="The unicode of the glyph, if you pass more than one, the anothers receive next codes. (Default: 61440)")
    parser.add_argument("--map-name", help="The name of the glyphmap file.")
    parser.add_argument("--map-format", default=map_formats["json"], choices=[map_formats["json"], map_formats["ts-enum"]], help="The type of the glyphmap file. (Default: json)")

    args = parser.parse_args()

    code = args.code
    list_glyphs = args.files
    map_name = args.map_name
    map_format = args.map_format
    output_file = args.output

    dict_glyphmaps = generateFont(output_file, list_glyphs, code)
    if map_name:
        generate_glyphmaps(dict_glyphmaps, map_name, map_format)
    exit(0)

def generateFont(outputFile, listGlyphs, codePoint):
    print 'glyph files: ' + str(len(listGlyphs))

    font = fontforge.font()
    font.fontname = os.path.splitext(os.path.basename(outputFile))[0]

    dict_glyphmaps = {}

    # add chars
    for fileName in listGlyphs:
        char = font.createChar(codePoint)
        char.importOutlines(fileName)

        # if importOutlines not changed the char, probably the char contains errors
        if not char.changed:
            print 'file with error: ' + fileName
            continue

        # align in left
        char.left_side_bearing = 0
        # set width
        x_max = char.boundingBox()[2]
        char.width = char.vwidth = x_max

        # add glyphmap
        basename = os.path.splitext(os.path.basename(fileName))[0]
        dict_glyphmaps[basename] = codePoint

        codePoint += 1

    font.generate(outputFile)
    print 'Generate font: ' + outputFile
    return dict_glyphmaps

def generate_glyphmaps(dict_glyphmaps, map_name, map_format):
    glyph_items = sorted(dict_glyphmaps.items(), key=itemgetter(1))

    file = open(map_name, "w+")

    text = None
    if map_format == map_formats["json"]:
        text = map_format_json(glyph_items)
    elif map_format == map_formats["ts-enum"]:
        text = map_format_ts_enum(glyph_items)

    if text == None:
        print "Error while generating the map file: {0}".format(map_name)
    else:
        file.write(text)
    file.close()

def map_format_json(glyph_items):
    text = "{\n"
    for item in glyph_items:
        key, value = item
        line_break = ",\n" if key != glyph_items[-1][0] else ""
        text += "    \"{0}\": {1}{2}".format(key, value, line_break)
    text += "\n}"
    return text

def map_format_ts_enum(glyph_items):
    text = "enum Map {\n"
    for item in glyph_items:
        key, value = item
        line_break = ",\n" if key != glyph_items[-1][0] else ","
        text += "    {0} = {1}{2}".format(key, value, line_break)
    text += "\n}"
    text += "\n\n"
    text += "export default Map\n"
    return text

if __name__ == "__main__":
    main(sys.argv)