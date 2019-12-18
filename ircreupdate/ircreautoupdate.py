#!/usr/bin/env python3
import sys
import os

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

from datetime import datetime


def openproxy():
    try:
        sshid = os.popen('''ps aux | grep 9524| grep ssh''').read().strip().split()[1]
    except:
        sshid = None
    if sshid is not None:
        os.system('''kill ''' + sshid)
    os.system('''/home/limingtao/bin/proxy.sh''')
    return 0


def bibtexfilecopy():
    dt = datetime.now()
    ircrebibwebsitefile = '/srv/main-websites/ircre/js/ircre.bib'
    currentdir = os.getcwd()
    os.system(
        '''cd ''' + currentdir + ''';''' +
        '''cp ''' + ircrebibwebsitefile + ''' ''' + currentdir + '''/ -f ; cp ircre.bib ircre'''
        + str(dt.year) + str(dt.month) + str(dt.day) + '''.bib;''')
    return 0


def bibtexclassify():
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False

    with open('ircre.bib', encoding='utf8') as bibtexfile:
        ircrebib_database = bibtexparser.load(bibtexfile, parser)

    allentries = ircrebib_database.entries.copy()
    # ----------------------------------------
    # get all articles
    # -----------------------------------------
    article_entries = []
    for i in range(len(allentries)):
        if allentries[i]['ENTRYTYPE'] == 'article':
            article_entries.append(allentries[i].copy())

    article_database = BibDatabase()
    article_database.entries = article_entries

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('order',)
    with open('articles.bib', 'w', encoding='utf8') as article_file:
        bibtexparser.dump(article_database, article_file, writer=writer)

    return 0


def articlessort():
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False

    with open('articles.bib', encoding='utf8') as articlesfile:
        articles_database = bibtexparser.load(articlesfile, parser)

    articles = articles_database.entries.copy()

    for i in range(len(articles)):
        try:
            articles[i]['sortkey1'] = float(articles[i]['impactfactor'])
        except:
            articles[i]['sortkey1'] = float(0)
        try:
            articles[i]['sortkey2'] = int(articles[i]['cited'])
        except:
            articles[i]['sortkey2'] = int(0)

    sorted_by_journalif_cited = sorted(articles, key=lambda x: (x['sortkey1'], x['sortkey2'], x['year']),
                                       reverse=True)

    for i in range(len(sorted_by_journalif_cited)):
        sorted_by_journalif_cited[i]['order'] = str(i).zfill(6)

    for i in range(len(sorted_by_journalif_cited)):
        sorted_by_journalif_cited[i].pop('sortkey1')
        sorted_by_journalif_cited[i].pop('sortkey2')

    sortedarticlesdatabase = BibDatabase()
    sortedarticlesdatabase.entries = sorted_by_journalif_cited

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('order',)
    with open('sorted-articles.bib', 'w', encoding='utf8') as sortedarticlesfile:
        bibtexparser.dump(sortedarticlesdatabase, sortedarticlesfile, writer=writer)

    return 0


def getop15articles():
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False

    with open('articles.bib', encoding='utf8') as article_file:
        article_database = bibtexparser.load(article_file, parser)

    article_entries = article_database.entries.copy()

    for i in range(len(article_entries)):
        try:
            article_entries[i]['sortkey1'] = int(article_entries[i]['cited'])
        except:
            article_entries[i]['sortkey1'] = int(0)

    articles_sorted_by_cited = sorted(article_entries, key=lambda x: (x['sortkey1']), reverse=True)

    top15articles = []
    for i in range(15):
        top15articles.append(articles_sorted_by_cited[i].copy())

    for i in range(len(top15articles)):
        top15articles[i]['ENTRYTYPE'] = 'toparticle'
        top15articles[i]['ID'] = top15articles[i]['ID'] + 'a'

    for i in range(len(top15articles)):
        top15articles[i].pop('sortkey1')

    top15_database = BibDatabase()
    top15_database.entries = top15articles

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = None

    with open('top15.bib', 'w', encoding='utf8') as top15_file:
        bibtexparser.dump(top15_database, top15_file, writer=writer)
    return 0


def getclusterid(title, author):
    parser = BibTexParser(common_strings=False)
    parser.ignore_nonstandard_types = False

    with open('articles.bib', encoding='utf8') as article_file:
        article_database = bibtexparser.load(article_file, parser)

    article_entries = article_database.entries.copy()

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
        bibtexparser.dump(bib_database, newbibfile, writer=writer)

    return 0


def ircrebibmerge():
    articlesparser = BibTexParser(common_strings=False)
    articlesparser.ignore_nonstandard_types = False

    with open('sorted-articles.bib', encoding='utf8') as sortedarticle_file:
        sortedarticle_database = bibtexparser.load(sortedarticle_file, articlesparser)

    sortedarticles = sortedarticle_database.entries.copy()

    top15parser = BibTexParser(common_strings=False)
    top15parser.ignore_nonstandard_types = False

    with open('top15.bib', encoding='utf8') as top15_file:
        top15_database = bibtexparser.load(top15_file, top15parser)

    top15articles = top15_database.entries.copy()

    alldb = BibDatabase()
    entries = []

    for i in range(len(top15articles)):
        entries.append(top15articles[i].copy())

    for i in range(len(sortedarticles)):
        entries.append(sortedarticles[i].copy())

    alldb.entries = entries

    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = None

    with open('newircre.bib', 'w', encoding='utf8') as newircrebibfile:
        bibtexparser.dump(alldb, newircrebibfile, writer=writer)

    return 0


def getcitation():
    articlesparser = BibTexParser(common_strings=False)
    articlesparser.ignore_nonstandard_types = False
    with open('articles.bib', encoding='utf8') as articlesfile:
        articles_database = bibtexparser.load(articlesfile, articlesparser)

    articleentries = articles_database.entries

    for n in range(len(articleentries) - 100):
        i = n + 100
        print("---------------------------")
        print("Entry number: " + str(i))
        title = articleentries[i]['title']
        clusterid = articleentries[i]['clusterid']
        print("Title: " + title)
        print("Cluster ID: " + clusterid)

        if not clusterid == "unknown":
            print(str(i))
            try:
                citations = os.popen(
                    '''./scholarpy/scholar.py -c 1 -C ''' + clusterid + ''' |grep -v list |grep Citations''').read().strip().split()[
                    -1]
            except:
                citations = "unknown"
        else:
            citations = "unknown"

        print("new Citations: " + citations)

        if 'cited' in articleentries[i]:
            oldcitednumber = int(articleentries[i]['cited'])
        else:
            oldcitednumber = 0

        print("Old Cited Number: " + str(oldcitednumber))

        if not citations == "unknown":
            citednumber = int(citations)
            if citednumber > oldcitednumber and ((citednumber - oldcitednumber) < 8):
                articleentries[i]['cited'] = str(citednumber)

        writer = BibTexWriter()
        writer.indent = '    '
        writer.order_entries_by = ('order',)

        with open('cited-add-articles.bib', 'w', encoding='utf8') as newarticlefile:
            bibtexparser.dump(articles_database, newarticlefile, writer=writer)

        os.popen("cp cited-add-ircre.bib tempcited-add-ircre.bib")

    with open('cited-add-articles.bib', 'w', encoding='utf8') as newarticlefile:
        bibtexparser.dump(articles_database, newarticlefile, writer=writer)

    return 0


def entryadd(doi):
    pass


def updatestatistics():
    pass


def main():
    openproxy()

    # 从网站目录复制bib文件
    bibtexfilecopy()

    # 分类，分成article.bib, bookchapter.bib, ...
    bibtexclassify()

    # entryadd()

    # getclusterid()

    # 更新引用次数
    getcitation()

    # 按影响因子和引用次数对article排序，并取出top 15 most cited articles，
    articlessort()

    getop15articles()

    # 合并文件
    ircrebibmerge()

    updatestatistics()

    return 0


if __name__ == '__main__':
    sys.exit(main())