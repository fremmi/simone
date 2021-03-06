import sys
import xmltodict
import dicttoxml

import requests
import json


def parse_line(line):
    data = line.split(";")
    if len(data) >= 2:
        return data[0], data[1]
    else:
        print("Could not parse line {}".format(line))
        return None, None


def create_csv(dict) :
    csv = ""
    sep = "|"
    for key in dict:
        line = ""
        if not 'scheda' in dict[key]["root"]:
            print("Key 'scheda' not found in dict ")
            continue

        codiceproduttore = dict[key]["root"]["scheda"]["codiceproduttore"]
        ean = dict[key]["root"]["scheda"]["ean"]
        catmerc = dict[key]["root"]["scheda"]["catmerc"]
        descrizione = dict[key]["root"]["scheda"]["descrizione"].replace('\n', " ")

        if codiceproduttore == None or catmerc == None:
            continue

        if ean == None:
            ean = " "

        line += codiceproduttore + sep + ean + sep + catmerc + sep + descrizione + sep

        for block_dict in dict[key]["root"]["quickinfo"]["titolo"]:
            block_descrizione = "@" + block_dict["descrizione"] + "@"
            line += block_descrizione + sep
            for elem in block_dict["quick"]:
                for k in elem:
                    if k == "descrizione":
                        elem_descrizione = elem[k]
                    elif k == "valore":
                        elem_valore = elem[k].replace('\n'," ")

                line += elem_descrizione + sep + elem_valore + sep

        csv += line + '\n'
    return csv


def main():
    if len(sys.argv) < 3:
        print ("Usage: scrape link_file output_file")
        exit(0)

    link_file = sys.argv[1]
    output_file = sys.argv[2]
    dict = {}
    f = open(link_file, "r+")
    o = open(output_file, "w+")
    url_count = 0
    for line in f:
        if line.__contains__("Column") or line == None:
            continue
        code, url_code = parse_line(line)
        url = "http://it.esprinet.com/schedeServizioDati/?" + url_code

        if code != None and url != None:
            r = requests.get(url, auth=requests.auth.HTTPBasicAuth("1-W26813", "H1dYhvsCIlfi1RsbuiWt"))
            # print("status: {} / text: {}".format(r.status_code, r.text))
            if len(r.text):
                dict[code] = xmltodict.parse(r.text)
                url_count = url_count+1
            else:
                print("Error getting url {}".format(url))

    # print(json.dumps(dict))
    # o.write(dicttoxml.dicttoxml(dict))
    csv = create_csv(dict)
    o.write(csv)
    print("Analyzed {} urls".format(url_count))
    # print(csv)


if __name__ == "__main__":
    main()
