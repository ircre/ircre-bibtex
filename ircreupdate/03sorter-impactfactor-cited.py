#!/usr/bin/env python3
import os
import sys
from operator import itemgetter
from bibtexparser.bibdatabase import BibDatabase


def main():
    import bibtexparser
    from bibtexparser.bwriter import BibTexWriter
    with open('cited-add-ircre.bib', encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    entries = bib_database.entries.copy()
    for i in range(len(entries)):
        try:
            entries[i]['sortkey1'] = float(entries[i]['impactfactor'])
        except:
            entries[i]['sortkey1'] = float(0)
        try:
            entries[i]['sortkey2'] = float(entries[i]['cited'])
        except:
            entries[i]['sortkey2'] = float(0)

    sorted_by_journalimpactor_cited = sorted(entries, key=lambda x: (x['sortkey1'], x['sortkey2'], x['year']),
                                             reverse=True)

    for i in range(len(sorted_by_journalimpactor_cited)):
        sorted_by_journalimpactor_cited[i]['order'] = str(i).zfill(6)

    for i in range(len(sorted_by_journalimpactor_cited)):
        sorted_by_journalimpactor_cited[i].pop('sortkey1')
        sorted_by_journalimpactor_cited[i].pop('sortkey2')

    newbibtexdatabase = BibDatabase()
    newbibtexdatabase.entries = sorted_by_journalimpactor_cited
    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('order',)

    with open('sorted-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(newbibtexdatabase, newbibfile, writer=writer)

    return 0


if __name__ == '__main__':
    sys.exit(main())
