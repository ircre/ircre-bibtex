#!/usr/bin/env python3
import os
import sys


def main():
    import bibtexparser
    from bibtexparser.bwriter import BibTexWriter

    with open('ircre.bib', encoding='utf8') as bibtex_file:
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
        if entries[i]['clusterid'] == 'unknown':
            print("---------------------------")
            print("Entry number: " + str(i))
            title = entries[i]['title']
            print("Title: " + title)
            clusterid = ''
            try:
                clusterid = os.popen(
                    '''./scholarpy/scholar.py -c 1 -t --phrase="''' + title + '''" |grep ID| grep Cluster''').read().strip().split()[
                    -1]
            except:
                clusterid = "unknown"

            print("new Cluster ID: " + clusterid)
            entries[i]['clusterid'] = clusterid
        with open('clusterid-added-ircre.bib', 'w', encoding='utf8') as newbibfile:
            bibtexparser.dump(bib_database, newbibfile, writer=writer)
        os.popen("cp clusterid-added-ircre.bib tempclusterid-added-ircre.bib")


    with open('clusterid-added-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(bib_database, newbibfile, writer = writer)

    return 0




if __name__ == '__main__':
    sys.exit(main())
