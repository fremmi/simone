import sys
import xmltodict
import dicttoxml

import requests


def parse_line(line):
    data = line.split(";")
    if len(data) >= 3:
        return data[0], data[2]
    else:
        return None, None

def main():
    if len(sys.argv) < 3:
        print ("Usage: scrape link_file output_file")
        exit(0)

    link_file = sys.argv[1]
    output_file = sys.argv[2]
    dict = {}
    f = open(link_file, "r+")
    o = open(output_file, "w+")
    for line in f:
        if line.__contains__("Column") or line == None:
            continue
        code, url = parse_line(line)

        if code != None and url != None:
            r = requests.get(url, auth=requests.auth.HTTPBasicAuth("1-W26813", "H1dYhvsCIlfi1RsbuiWt"))
            # print("SUCUNI {}".format(r.status_code))
            if len(r.text):
                dict[code] = xmltodict.parse(r.text)

    o.write(dicttoxml.dicttoxml(dict))

if __name__ == "__main__":
    main()
