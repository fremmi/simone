import sys
import xmltodict
import dicttoxml

import requests
import json


def parse_line(line):
    data = line.split(";")
    if len(data) >= 3:
        return data[0], data[2]
    else:
        return None, None


def create_csv(dict) :
    csv = ""
    for key in dict:
        line = ""
        codiceproduttore = dict[key]["root"]["scheda"]["codiceproduttore"]
        ean = dict[key]["root"]["scheda"]["ean"]
        catmerc = dict[key]["root"]["scheda"]["catmerc"]
        descrizione = dict[key]["root"]["scheda"]["descrizione"]

        line += codiceproduttore + ";" + ean + ";" + catmerc + ";" + descrizione + ";"

        for block_dict in dict[key]["root"]["quickinfo"]["titolo"]:
            block_descrizione = "@" + block_dict["descrizione"] + "@"
            line += block_descrizione + ";"
            for elem in block_dict["quick"]:
                print(elem)
                # elem_descrizione = elem["descrizione"]
                # elem_valore = elem["valore"]
                # line += elem_descrizione + ";" + elem_valore

        csv += line + "\n"


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
            # print("status: {} / text: {}".format(r.status_code, r.text))
            if len(r.text):
                dict[code] = xmltodict.parse(r.text)

    # print(json.dumps(dict))
    # o.write(dicttoxml.dicttoxml(dict))
    csv = create_csv(dict)
    o.write(csv)
    print(csv)


if __name__ == "__main__":
    main()
