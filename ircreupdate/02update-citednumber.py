#!/usr/bin/env python3
import os
import sys


def main():
    import bibtexparser
    from bibtexparser.bwriter import BibTexWriter

    with open('clusterid-added-ircre.bib', encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    entries = bib_database.entries
    print("---------------------------")
    print("---------------------------")
    print("---------------------------")
    print("Total articles number: " + str(len(entries)))
    print("---------------------------")
    print("---------------------------")
    print("---------------------------")

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('order',)

    for i in range(len(entries)):
        print("---------------------------")
        print("Entry number: " + str(i))
        title = entries[i]['title']
        clusterid = entries[i]['clusterid']
        print("Title: " + title)
        print("Cluster ID: " + clusterid)

        if not clusterid == "unknown":
            print("hello" + str(i))
            try:
                citations = os.popen(
                    '''./scholarpy/scholar.py -c 1 -C ''' + clusterid + ''' |grep -v list |grep Citations''').read().strip().split()[
                    -1]
            except:
                citations = "unknown"
        else:
            citations = "unknown"


        print("new Citations: " + citations)

        if 'cited' in entries[i]:
            oldcitednumber = int(entries[i]['cited'])
        else:
            oldcitednumber = 0

        print("Old Cited Number: " + str(oldcitednumber))

        if not citations == "unknown":
            citednumber = int(citations)
            if citednumber > oldcitednumber:
                entries[i]['cited'] = str(citednumber)

        with open('cited-add-ircre.bib', 'w', encoding='utf8') as newbibfile:
            bibtexparser.dump(bib_database, newbibfile, writer=writer)
        os.popen("cp cited-add-ircre.bib tempcited-add-ircre.bib")


    with open('cited-add-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(bib_database, newbibfile, writer = writer)

    return 0



if __name__ == '__main__':
    sys.exit(main())
