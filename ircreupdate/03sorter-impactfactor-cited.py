#!/usr/bin/env python3
import os
import sys
from bibtexparser.bibdatabase import BibDatabase


def main():
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter

    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('order',)

    try:
        os.remove('sorted-high.bib')
    except:
        a = open('sorted-high.bib', 'a', encoding='utf8')
        a.close()

    # ----------------------------------------
    # get all entries
    # -----------------------------------------

    with open('ircre.bib', encoding='utf8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file, parser)

    entries = bib_database.entries.copy()


    # ----------------------------------------
    # get all articles
    # -----------------------------------------

    articleentries = []

    for i in range(len(entries)):
        if entries[i]['ENTRYTYPE'] == 'article':
            articleentries.append(entries[i].copy())

    article_ircredatabase = BibDatabase()
    article_ircredatabase.entries = articleentries

    with open('articles-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(article_ircredatabase, newbibfile, writer=writer)

    # ----------------------------------------
    # sort all articles by cited (reverse)
    # -----------------------------------------

    for i in range(len(articleentries)):
        try:
            articleentries[i]['sortkey1'] = int(articleentries[i]['cited'])
        except:
            articleentries[i]['sortkey1'] = int(0)

    articles_sorted_by_cited = sorted(articleentries, key=lambda x: (x['sortkey1']), reverse=True)


    toparticles = []

    for i in range(15):
        toparticles.append(articles_sorted_by_cited[i].copy())

    for i in range(len(toparticles)):
        toparticles[i]['ENTRYTYPE'] = 'toparticle'
        toparticles[i]['ID'] = toparticles[i]['ID'] + 'a'

    for i in range(len(toparticles)):
        toparticles[i].pop('sortkey1')

    top15database = BibDatabase()
    top15database.entries = toparticles

    writer.order_entries_by = ('cited',)


    with open('top15-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(top15database, newbibfile, writer=writer)


    for i in range(len(articleentries)):
         articleentries[i].pop('sortkey1')

    for i in range(len(articleentries)):
        try:
            articleentries[i]['sortkey1'] = float(articleentries[i]['impactfactor'])
        except:
            articleentries[i]['sortkey1'] = float(0)
        try:
            articleentries[i]['sortkey2'] = int(articleentries[i]['cited'])
        except:
            articleentries[i]['sortkey2'] = int(0)


    sorted_by_journalimpactor_cited = sorted(articleentries, key=lambda x: (x['sortkey1'], x['sortkey2'], x['year']), reverse=True)

    for i in range(len(sorted_by_journalimpactor_cited)):
        sorted_by_journalimpactor_cited[i]['order'] = str(i).zfill(6)

    for i in range(len(sorted_by_journalimpactor_cited)):
        sorted_by_journalimpactor_cited[i].pop('sortkey1')
        sorted_by_journalimpactor_cited[i].pop('sortkey2')

    sortedarticledatabase = BibDatabase()
    sortedarticledatabase.entries = sorted_by_journalimpactor_cited

    writer.order_entries_by = ('order',)
    with open('sorted-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(sortedarticledatabase, newbibfile, writer=writer)


    alldb = BibDatabase()
    entries = []

    for i in range(len(toparticles)):
        entries.append(toparticles[i].copy())

    for i in range(len(sorted_by_journalimpactor_cited)):
        entries.append(sorted_by_journalimpactor_cited[i].copy())

    print(entries[14])
    print(entries[15])
    alldb.entries = entries
    writer.order_entries_by = None

    with open('top15-sorted-ircre.bib', 'w', encoding='utf8') as newbibfile:
        bibtexparser.dump(alldb, newbibfile, writer=writer)


    return 0


if __name__ == '__main__':
    sys.exit(main())
