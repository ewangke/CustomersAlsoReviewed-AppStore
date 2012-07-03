import json
import sys
import unicodecsv
import codecs

if len(sys.argv) != 2:
    print 'Usage: convert.py <filename.json>'
    exit(0)

input_file = sys.argv[1]


def convert(input_file):
    l = json.load(codecs.open(input_file, 'r', 'utf-8'))
    output_file = input_file.replace(".json", ".csv")
    csv_writer = unicodecsv.writer(open(output_file, 'w'))
    for item in l:
        csv_writer.writerow(item)


if __name__ == "__main__":
    convert(input_file)
